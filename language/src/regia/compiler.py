"""
Compiler pipeline for the Regia compiler.

Orchestrates preprocessing, parsing, AST building, validation,
and emission. Each stage only runs if the previous produced zero
errors. This module contains no grammar or emission logic; it is
pure pipeline wiring.

Supports both single-file and multi-file compilation. In multi-file
mode each file is preprocessed, parsed, and built independently,
then the resulting AST Programs are merged into a single Program for
validation and emission.

The IMPORT resolution introduced in v0.2 is transparent: calling
compile_file() on a file with IMPORT statements automatically
resolves all dependencies and delegates to the multi-file path.

Pipeline stages
---------------
  0. Preprocess  (extract doc comments, resolve IMPORT graph)
  1. Parse       (source string to Lark tree)
  2. Build       (Lark tree to typed AST)
  3. Annotate    (attach doc comments to AST nodes)
  4. Validate    (semantic checks on AST)
  5. Emit        (AST to AgentSpeak strings)
"""

from __future__ import annotations

import sys

from dataclasses import dataclass, field
from pathlib     import Path
from typing      import Dict, List, Optional, Union

from lark import UnexpectedToken, UnexpectedCharacters

from regia.parser        import parse
from regia.ast_builder   import ASTBuilder
from regia.ast_nodes     import (
    DocAnnotation, ImportDecl,
    ActionDecl, EventDecl, FactDecl, PlaybookDef, PlotDef,
    Program,
)
from regia.errors        import ErrorReporter, CompilerMessage
from regia.preprocessor  import preprocess, resolve_imports, SourceAnnotations
from regia.syntax_errors import report_syntax_error
from regia.validator     import Validator
from regia.emitter       import Emitter


# == Result type ===============================================================

@dataclass
class CompileResult:
    """The result of compiling one or more Regia source files.

    Attributes:
        success:       True if compilation completed without errors.
        outputs:       Mapping of agent name to generated AgentSpeak string.
        error_count:   Total number of errors encountered.
        warning_count: Total number of warnings encountered.
        messages:      List of all compiler diagnostics.
        ast:           Compiled Abstract Syntax Tree (for the editor server).
    """

    success:       bool
    outputs:       Dict[str, str]
    error_count:   int
    warning_count: int
    messages:      List[CompilerMessage]
    ast:           Optional[Program] = None


# == Public API ================================================================

def compile_source(
    source:   str,
    filename: str = "<string>",
    emit:     bool = True,
) -> CompileResult:
    """Compile a Regia source string through the full pipeline.

    Note: IMPORT statements inside a raw source string cannot be
    resolved (there is no file system context). If the source contains
    IMPORTs they will parse successfully but the imported files will
    not be included. Use compile_file() to get IMPORT resolution.

    Stages:
        0. Preprocess (extract doc comments; IMPORTs noted but not resolved)
        1. Parse    (source string to Lark tree)
        2. Build    (Lark tree to typed AST)
        3. Annotate (attach doc comments to AST nodes)
        4. Validate (semantic checks on AST)
        5. Emit     (AST to AgentSpeak strings)

    Args:
        source:   The Regia source code as a string.
        filename: Optional filename for diagnostics (defaults to '<string>').
        emit:     If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    reporter = ErrorReporter()

    # == Stage 0: Preprocess ===================================================
    annotations = preprocess(source, filename=filename)
    reporter.register_source(filename, annotations.clean_source) # register source to later give context to the error reporter

    # == Stage 1: Parse ========================================================
    try:
        tree = parse(annotations.clean_source) # parse the clean source
    except (UnexpectedToken, UnexpectedCharacters) as e:
        report_syntax_error(e, reporter, filename=filename) # report syntax error
        return _failure(reporter) # return failure

    # == Stage 2: Build AST ====================================================
    builder = ASTBuilder(filename=filename) # builder is a lark transformer

    program: Program = builder.transform(tree) # transform the tree to an AST
    if reporter.has_errors(): # if there are errors after building the AST, return failure
        return _failure(reporter)

    # == Stage 3: Annotate =====================================================
    _attach_doc_comments(program, annotations.doc_comments) # attach doc comments to AST nodes

    # == Stage 4: Validate =====================================================
    validator = Validator(reporter) # validator checks for semantic errors

    validator.validate(program) # validate the AST
    if reporter.has_errors(): # if there are errors after validation, return failure
        return _failure(reporter)

    # == Stage 5: Emit AgentSpeak ==============================================
    outputs: Dict[str, str] = {}
    if emit:
        emitter = Emitter()
        outputs = emitter.emit(program)

    return CompileResult(
        success       = True,
        outputs       = outputs,
        error_count   = reporter.error_count,
        warning_count = reporter.warning_count,
        messages      = reporter.messages,
        ast           = program,
    )


def compile_file(
    filepath: Union[str, Path],
    emit:     bool = True,
) -> CompileResult:
    """Compile a single .regia file through the full pipeline.

    If the file contains IMPORT statements, they are resolved and all
    dependent files are compiled together (delegating to compile_files).

    Args:
        filepath: Path to the Regia source file.
        emit:     If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    filepath = Path(filepath).resolve()
    reporter = ErrorReporter()

    # Quick pre-scan: resolve the full import graph starting from this file.
    all_files = resolve_imports(
        filepath,
        reporter_cb=lambda msg, fpath: reporter.error(
            0, 0, 1, msg, filename=fpath.name if fpath else "",
        ),
    )

    if reporter.has_errors():
        return _failure(reporter)

    # If there is only this file (no imports), use the single-file path
    # for a simpler, slightly faster pipeline.
    if len(all_files) == 1:
        source = filepath.read_text(encoding="utf-8")
        return compile_source(source, filename=filepath.name, emit=emit)

    # Multiple files (import graph): delegate to the multi-file pipeline.
    return compile_files(all_files, emit=emit)


def compile_files(
    filepaths: List[Path],
    emit:      bool = True,
) -> CompileResult:
    """Compile multiple .regia files through the full pipeline.

    Each file is preprocessed, parsed, and built into a Program
    independently. The Programs are then merged into one combined
    Program for validation and emission. File order does not matter
    for correctness (declarations are merged into a shared namespace).

    Stages:
        0. Preprocess each file (extract doc comments)
        1. Parse each file (continue on error to report all failures)
        2. Build AST for each file
        3. Annotate each Program with its doc comments
        4. Merge all Programs into one
        5. Validate merged Program
        6. Emit AgentSpeak

    Args:
        filepaths: List of paths to Regia source files.
        emit:      If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    # Single file: delegate to the simpler path
    if len(filepaths) == 1:
        return compile_file(filepaths[0], emit=emit)

    reporter  = ErrorReporter()
    programs: List[Program] = []

    # == Stages 0, 1 & 2: Preprocess + Parse + Build each file ================
    for fpath in filepaths:
        filename = fpath.name
        raw_source = fpath.read_text(encoding="utf-8")

        # Stage 0: Preprocess
        annotations = preprocess(raw_source, filename=filename)
        reporter.register_source(filename, annotations.clean_source)

        # Stage 1: Parse
        try:
            tree = parse(annotations.clean_source)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            report_syntax_error(e, reporter, filename=filename)
            continue  # Try remaining files to report all errors at once

        # Stage 2: Build
        builder = ASTBuilder(filename=filename)
        program: Program = builder.transform(tree)

        # Stage 3: Annotate this file's Program
        _attach_doc_comments(program, annotations.doc_comments)

        programs.append(program)

    # If any file failed to parse, stop here
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 4: Merge Programs ===============================================
    merged = Program()
    for prog in programs:
        merged.items.extend(prog.items)
        merged.doc_comments.extend(prog.doc_comments)

    # == Stage 5: Validate =====================================================
    validator = Validator(reporter)
    validator.validate(merged)
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 6: Emit =========================================================
    outputs: Dict[str, str] = {}
    if emit:
        emitter = Emitter()
        outputs = emitter.emit(merged)

    return CompileResult(
        success       = True,
        outputs       = outputs,
        error_count   = reporter.error_count,
        warning_count = reporter.warning_count,
        messages      = reporter.messages,
    )


def parse_files(filepaths: List[Path]) -> Program:
    """Parse one or more files and return the merged AST.

    Stops after AST building, without validation or emission.
    Prints parsing errors to stdout and exits if there are any,
    otherwise returns the merged Program.

    Args:
        filepaths: List of paths to Regia source files.

    Returns:
        The merged Program AST.
    """
    reporter  = ErrorReporter()
    programs: List[Program] = []

    for fpath in filepaths:
        filename   = fpath.name
        raw_source = fpath.read_text(encoding="utf-8")

        annotations = preprocess(raw_source, filename=filename)
        reporter.register_source(filename, annotations.clean_source)

        try:
            tree = parse(annotations.clean_source)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            report_syntax_error(e, reporter, filename=filename)
            continue

        builder = ASTBuilder(filename=filename)
        program: Program = builder.transform(tree)
        _attach_doc_comments(program, annotations.doc_comments)
        programs.append(program)

    if reporter.has_errors():
        print(reporter.format_all())
        print(f"\nParsing failed with {reporter.error_count} error(s).")
        sys.exit(1)

    merged = Program()
    for prog in programs:
        merged.items.extend(prog.items)
        merged.doc_comments.extend(prog.doc_comments)
    return merged


# == Internal ==================================================================

# Nodes that can have doc annotations attached to them.
_ANNOTATABLE = (ActionDecl, EventDecl, FactDecl, PlaybookDef, PlotDef)


def _attach_doc_comments(
    program:  Program,
    doc_comments: List[DocAnnotation],
) -> None:
    """Attach #@ doc annotations to the AST nodes they precede.

    Annotations are matched to top-level nodes by source line proximity:
    a doc comment group belongs to the next top-level item whose
    source line is greater than the comment's line. File-level
    annotations (those before all items) are stored on Program itself.

    Modifies program and its items in-place.

    Args:
        program:      The root AST node to annotate.
        doc_comments: Ordered list of annotations from the preprocessor.
    """
    if not doc_comments:
        return

    # Build a sorted list of (item_line, item) for annotatable nodes
    items_with_lines: List[tuple] = []
    for item in program.items:
        if isinstance(item, _ANNOTATABLE):
            loc = getattr(item, "loc", None)
            line = loc.line if loc else 0
            if line > 0:
                items_with_lines.append((line, item))

    items_with_lines.sort(key=lambda t: t[0])

    # Group annotations and assign each group to the nearest subsequent item
    pending: List[DocAnnotation] = []

    for annotation in doc_comments:
        # Find the first item that starts after this annotation's line
        target = None
        for item_line, item in items_with_lines:
            if item_line > annotation.line:
                target = item
                break

        if target is not None:
                target.docs.append(annotation)
        else:
            # No subsequent item: this is a file-level annotation
            program.doc_comments.append(annotation)


def _failure(reporter: ErrorReporter) -> CompileResult:
    """Build a failed CompileResult from the current reporter state.

    Args:
        reporter: The ErrorReporter containing collected diagnostics.

    Returns:
        A CompileResult with success=False.
    """
    return CompileResult(
        success       = False,
        outputs       = {},
        error_count   = reporter.error_count,
        warning_count = reporter.warning_count,
        messages      = reporter.messages,
    )
