"""
Preprocessor for the Regia compiler.

Runs before Lark parsing as the new first stage of the pipeline.
It is responsible for two tasks that both require scanning the raw
source text before the grammar sees it:

    1. Doc-comment extraction (#@ annotations)
       Strips #@ lines from the source, preserving line numbers by
       replacing them with blank lines, and returns the annotation
       objects so they can be attached to AST nodes after building.

    2. Import resolution (IMPORT "path" statements)
       Resolves the import graph starting from an entry file, detects
       circular dependencies, and returns the ordered list of file
       paths to feed into the multi-file compilation pipeline.

Both tasks produce a *clean* source string with the preprocessed
constructs removed, so the Lark grammar remains unchanged and
unaware of them.
"""

from __future__ import annotations

import re

from collections import deque
from dataclasses import dataclass, field
from pathlib     import Path
from typing      import Deque, Dict, List, Optional, Set, Tuple


# == Constants =================================================================

# Matches a doc-comment line: #@ followed by key, colon, optional value.
# Group 1 = key identifier, Group 2 = value text (may be empty).
_DOC_RE = re.compile(r"^\s*#@([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*?)\s*$")

# Matches a doc-comment continuation line: #- optional value.
# Group 1 = value text (may be empty).
_DOC_CONT_RE = re.compile(r"^\s*#-\s*(.*?)\s*$")

# Matches an IMPORT statement line: IMPORT "path".
# Group 1 = the path string (without surrounding quotes).
_IMPORT_RE = re.compile(r'^\s*IMPORT\s+"([^"]+)"\s*\.\s*$')


# == Doc annotations ===========================================================

@dataclass
class DocAnnotation:
    """A single #@ doc comment annotation from a source file.

    Attributes:
        key:      The annotation key (e.g. 'name', 'description').
        value:    The annotation value (freeform text).
        line:     The 1-based source line where this annotation was found.
        filename: The source file name.
    """

    key:      str
    value:    str
    line:     int
    filename: str = ""


# == Source annotations ========================================================

@dataclass
class SourceAnnotations:
    """Results of preprocessing a single source file.

    Attributes:
        clean_source: The source text with all preprocessor constructs
                      replaced by blank lines (line numbers preserved).
        doc_comments: All extracted #@ annotations in source order.
        import_paths: All IMPORT paths in source order (unresolved,
                      relative to the file's directory).
    """

    clean_source: str
    doc_comments: List[DocAnnotation] = field(default_factory=list)
    import_paths: List[str]           = field(default_factory=list)


# == Public API ================================================================

def preprocess(source: str, filename: str = "") -> SourceAnnotations:
    """Preprocess a Regia source string.

    Scans the source line by line, extracting #@ doc comments, #- continuations,
    and IMPORT statements. All are replaced with blank lines so that
    the Lark parser sees a clean source with unchanged line numbers.

    Args:
        source:   The raw Regia source code as a string.
        filename: The source file name (embedded in annotations).

    Returns:
        A SourceAnnotations with the cleaned source, doc comments,
        and import paths (in source order).
    """
    doc_comments: List[DocAnnotation] = []
    import_paths: List[str]           = []
    clean_lines:  List[str]           = []
    
    last_doc_idx: Optional[int] = None

    for line_num, raw_line in enumerate(source.splitlines(), start=1):
        doc_match      = _DOC_RE.match(raw_line)
        doc_cont_match = _DOC_CONT_RE.match(raw_line)
        import_match   = _IMPORT_RE.match(raw_line)

        if doc_match:
            doc_comments.append(DocAnnotation(
                key      = doc_match.group(1),
                value    = doc_match.group(2),
                line     = line_num,
                filename = filename,
            ))
            last_doc_idx = len(doc_comments) - 1
            clean_lines.append("")  # Preserve line number
        elif doc_cont_match:
            if last_doc_idx is not None:
                doc_comments[last_doc_idx].value += "\n" + doc_cont_match.group(1)
            clean_lines.append("")  # Preserve line number
        elif import_match:
            import_paths.append(import_match.group(1))
            last_doc_idx = None
            clean_lines.append("")  # Preserve line number
        else:
            if raw_line.strip() != "":
                last_doc_idx = None
            clean_lines.append(raw_line)

    # Preserve trailing newline behaviour of the original source
    clean_source = "\n".join(clean_lines)
    if source.endswith("\n"):
        clean_source += "\n"

    return SourceAnnotations(
        clean_source = clean_source,
        doc_comments = doc_comments,
        import_paths = import_paths,
    )


def resolve_imports(
    entry_file:  Path,
    reporter_cb: "ImportErrorCallback",
) -> List[Path]:
    """Resolve the import graph starting from entry_file.

    Performs a breadth-first walk of the import graph. Each file is
    preprocessed to extract its IMPORT declarations. The result is a
    list of absolute paths. Each file appears at most once.

    Circular imports are detected and reported via reporter_cb; the
    offending file is skipped so resolution continues.

    Missing files are also reported via reporter_cb.

    Args:
        entry_file:  The absolute path to the entry-point .regia file.
        reporter_cb: Callable that accepts (message: str, filepath: Path)
                     and records the error. Usually wraps ErrorReporter.

    Returns:
        Ordered list of absolute file paths to compile. Includes the
        entry file itself.
    """
    entry_abs = entry_file.resolve()

    # Maps each file to the file that imported it (for cycle reporting).
    imported_from: Dict[Path, Optional[Path]] = {entry_abs: None}

    # BFS queue of (file_to_process, importing_file_or_None)
    queue: Deque[Tuple[Path, Optional[Path]]] = deque()
    queue.append((entry_abs, None))

    # Preserves insertion order (Python 3.7+).
    # We use a list so we can control dependency ordering.
    visit_order: List[Path] = []

    while queue:
        current, from_file = queue.popleft()

        if not current.exists():
            msg = (
                f"Imported file not found: '{current}'"
                + (f" (imported from '{from_file.name}')" if from_file else "")
            )
            reporter_cb(msg, from_file or entry_abs)
            continue

        if current in [p for p in visit_order]:
            # Already processed, skip (idempotent imports).
            continue

        # Extract imports from this file
        try:
            raw_source = current.read_text(encoding="utf-8")
        except OSError as exc:
            reporter_cb(
                f"Cannot read imported file '{current}': {exc}",
                from_file or entry_abs,
            )
            continue

        annotations = preprocess(raw_source, filename=current.name)
        visit_order.append(current)

        for rel_path_str in annotations.import_paths:
            child = (current.parent / rel_path_str).resolve()

            if child in imported_from:
                # Cycle detection
                reporter_cb(
                    f"Circular import detected: "
                    f"'{current.name}' imports '{child.name}' "
                    f"which is already in the import chain.",
                    current,
                )
                continue

            imported_from[child] = current
            queue.append((child, current))

    return visit_order


# == Internal types ============================================================

# Type alias for the error callback used in resolve_imports.
# Callable[[str, Path], None]
ImportErrorCallback = "callable[[str, Path], None]"
