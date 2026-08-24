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

from __future__ import annotations # allows the use of types as annotations

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
    PhaseDecl, RoleDecl, PbWhenBlock, BasePlotWhenBlock,
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
    ast:           Program | None = None


# == Public API ================================================================

def parse_source(
    source:   str,
    filename: str,
    reporter: ErrorReporter,
) -> Program | None:
    """Run Stages 0-3 (Preprocess, Parse, Build, Annotate) for a single string.

    Args:
        source:   The Regia source code as a string.
        filename: Filename for diagnostics.
        reporter: The shared ErrorReporter to use.

    Returns:
        The built AST Program, or None if parsing/building failed.
    """
    # == Stage 0: Preprocess ===================================================
    annotations = preprocess(source, filename=filename)
    reporter.register_source(filename, source)

    # == Stage 1: Parse ========================================================
    try:
        tree = parse(source)
    except (UnexpectedToken, UnexpectedCharacters) as e:
        report_syntax_error(e, reporter, filename=filename)
        return None

    # == Stage 2: Build AST ====================================================
    builder = ASTBuilder(filename=filename)
    program: Program = builder.transform(tree)
    if reporter.has_errors():
        return None

    # == Stage 3: Annotate =====================================================
    _attach_doc_comments(program, annotations.doc_comments)
    return program


def parse_files(
    filepaths: list[Path],
    reporter:  ErrorReporter,
) -> Program | None:
    """Run Stages 0-3 for multiple files and return the merged AST.

    Args:
        filepaths: List of paths to Regia source files.
        reporter:  The shared ErrorReporter to use.

    Returns:
        The merged Program AST, or None if any file failed to parse/build.
    """
    programs: list[Program] = []

    for fpath in filepaths:
        filename = fpath.name
        raw_source = fpath.read_text(encoding="utf-8")
        
        program = parse_source(raw_source, filename, reporter)
        if program is not None:
            programs.append(program)

    if reporter.has_errors():
        return None

    merged = Program()
    for prog in programs:
        merged.items.extend(prog.items)
        merged.doc_comments.extend(prog.doc_comments)
    return merged


def compile_source(
    source:   str,
    filename: str = "<string>",
    emit:     bool = True,
) -> CompileResult:
    """Compile a Regia source string through the full pipeline.

    Stages:
        0. Preprocess (extract doc comments)
        1. Parse      (source string to Lark tree)
        2. Build      (Lark tree to typed AST)
        3. Annotate   (attach doc comments to AST nodes)
        4. Validate   (semantic checks on AST)
        5. Emit       (AST to AgentSpeak strings)
    """
    reporter = ErrorReporter()
    program = parse_source(source, filename, reporter)

    if program is None or reporter.has_errors():
        return _failure(reporter)

    # == Stage 4: Validate =====================================================
    validator = Validator(reporter)
    validator.validate(program)
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 5: Emit =========================================================
    outputs: dict[str, str] = {}
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
    filepath: str | Path,
    emit:     bool = True,
) -> CompileResult:
    """Compile a .regia file (and all its imports) through the full pipeline.

    Args:
        filepath: Path to the entry Regia source file.
        emit:     If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    filepath = Path(filepath).resolve()
    reporter = ErrorReporter()

    # Pre-scan: resolve the full import graph starting from this file.
    all_files = resolve_imports(filepath, reporter=reporter)
    if reporter.has_errors():
        return _failure(reporter)

    # Delegate to parse_files for Stages 0-3 across all files.
    program = parse_files(all_files, reporter)
    
    if program is None or reporter.has_errors():
        return _failure(reporter)

    # == Stage 4: Validate =====================================================
    validator = Validator(reporter)
    validator.validate(program)
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 5: Emit =========================================================
    outputs: dict[str, str] = {}
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


# == Internal ==================================================================

# Nodes that can have doc annotations attached to them.
_ANNOTATABLE = (
    ActionDecl, EventDecl, FactDecl, PlaybookDef, PlotDef,
    PhaseDecl, RoleDecl, PbWhenBlock, BasePlotWhenBlock,
)

def _iter_annotatables(program: Program):
    """Yield all nodes in the AST that can receive doc annotations."""
    for item in program.items:
        if isinstance(item, _ANNOTATABLE):
            yield item
        
        if isinstance(item, PlaybookDef):
            yield from item.when_blocks
        
        elif isinstance(item, PlotDef):
            yield from item.roles
            yield from item.phases
            for during in item.during_blocks:
                yield from during.when_blocks


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
    for item in _iter_annotatables(program):
        loc = getattr(item, "loc", None)
        line = loc.line if loc else 0
        if line > 0:
            items_with_lines.append((line, item))

    items_with_lines.sort(key=lambda t: t[0])

    # Assign each annotation to the nearest subsequent item
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
