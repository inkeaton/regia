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

The raw source text is left unmodified, as the Lark grammar already
contains rules to parse IMPORTs and ignore doc-comments.
"""

from __future__ import annotations

import re

from collections import deque
from dataclasses import dataclass, field
from pathlib     import Path
from typing      import Deque, Dict, List, Optional, Set, Tuple

from regia.errors import ErrorReporter


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


@dataclass
class ImportDirective:
    """An IMPORT statement extracted from a source file.
    
    Attributes:
        path: The string path specified in the import.
        line: The 1-based source line where it was found.
    """
    path: str
    line: int


# == Source annotations ========================================================

@dataclass
class SourceAnnotations:
    """Results of preprocessing a single source file.

    Attributes:
        doc_comments: All extracted #@ annotations in source order.
        import_paths: All IMPORT paths in source order (unresolved,
                      relative to the file's directory).
    """

    doc_comments: List[DocAnnotation]   = field(default_factory=list)
    import_paths: List[ImportDirective] = field(default_factory=list)


# == Public API ================================================================

def preprocess(source: str, filename: str = "") -> SourceAnnotations:
    """Preprocess a Regia source string.

    Scans the source line by line, extracting #@ doc comments, #- continuations,
    and IMPORT statements.

    The raw source text is left unmodified, as the Lark grammar already
    contains rules to parse IMPORTs and ignore doc-comments.

    Args:
        source:   The raw Regia source code as a string.
        filename: The source file name (embedded in annotations).

    Returns:
        A SourceAnnotations with the doc comments and import paths (in source order).
    """
    doc_comments: List[DocAnnotation]   = []
    import_paths: List[ImportDirective] = []
    
    last_doc_idx: int | None = None

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
        elif doc_cont_match:
            if last_doc_idx is not None:
                doc_comments[last_doc_idx].value += "\n" + doc_cont_match.group(1)
        elif import_match:
            import_paths.append(ImportDirective(path=import_match.group(1), line=line_num))
            last_doc_idx = None
        else:
            if raw_line.strip() != "":
                last_doc_idx = None

    return SourceAnnotations(
        doc_comments = doc_comments,
        import_paths = import_paths,
    )


def resolve_imports(
    entry_file:  Path,
    reporter:    ErrorReporter,
) -> List[Path]:
    """Resolve the import graph starting from entry_file.

    Performs a breadth-first walk of the import graph. Each file is
    preprocessed to extract its IMPORT declarations. The result is a
    list of absolute paths. Each file appears at most once.

    Circular imports are detected and reported via the reporter; the
    offending file is skipped so resolution continues.

    Missing files are also reported via the reporter.

    Args:
        entry_file:  The absolute path to the entry-point .regia file.
        reporter:    The ErrorReporter instance to record diagnostics.

    Returns:
        Ordered list of absolute file paths to compile. Includes the
        entry file itself.
    """
    entry_abs = entry_file.resolve()

    # BFS queue of (file_to_process, importing_file_or_None, line_number_in_importing_file, ancestors_set)
    queue: Deque[Tuple[Path, Path | None, int, frozenset]] = deque()
    queue.append((entry_abs, None, 0, frozenset([entry_abs])))

    # Preserves insertion order (Python 3.7+).
    # We use a list so we can control dependency ordering.
    visit_order: List[Path] = []
    # We use a set for O(1) idempotency checks.
    visited: Set[Path] = set()

    while queue:
        current, from_file, import_line, ancestors = queue.popleft()

        if not current.exists():
            msg = (
                f"Imported file not found: '{current}'"
                + (f" (imported from '{from_file.name}')" if from_file else "")
            )
            reporter.error(
                import_line, 0, 1, msg,
                filename=from_file.name if from_file else entry_abs.name
            )
            continue

        if current in visited:
            # Already processed, skip (idempotent imports).
            continue

        # Extract imports from this file
        try:
            raw_source = current.read_text(encoding="utf-8")
        except OSError as exc:
            reporter.error(
                import_line, 0, 1,
                f"Cannot read imported file '{current}': {exc}",
                filename=from_file.name if from_file else entry_abs.name
            )
            continue

        annotations = preprocess(raw_source, filename=current.name)
        visit_order.append(current)
        visited.add(current)

        for imp_dir in annotations.import_paths:
            child = (current.parent / imp_dir.path).resolve()

            if child in ancestors:
                # Cycle detection
                reporter.error(
                    imp_dir.line, 0, 1,
                    f"Circular import detected: "
                    f"'{current.name}' imports '{child.name}' "
                    f"which is already in the import chain.",
                    filename=current.name,
                )
                continue

            queue.append((child, current, imp_dir.line, ancestors | frozenset([child])))

    return visit_order
