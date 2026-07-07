"""
Compiler pipeline for the Regia compiler.

Orchestrates parsing, AST building, validation, and emission.
Each stage only runs if the previous produced zero errors.
This module contains no grammar or emission logic; it is pure wiring.

Supports both single-file and multi-file compilation. In multi-file
mode, each file is parsed and built independently, then the resulting
AST Programs are merged into a single Program for validation and
emission.
"""

from dataclasses import dataclass
from pathlib     import Path
from typing      import Dict, List, Union

from lark import UnexpectedToken, UnexpectedCharacters

from regia.parser        import parse
from regia.ast_builder   import ASTBuilder
from regia.ast_nodes     import Program
from regia.errors        import ErrorReporter, CompilerMessage
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
    """

    success:       bool
    outputs:       Dict[str, str]
    error_count:   int
    warning_count: int
    messages:      List[CompilerMessage]


# == Core compile functions ====================================================

def compile_source(source: str, filename: str = "<string>", emit: bool = True) -> CompileResult:
    """Compile a Regia source string through the full pipeline.

    Stages:
        1. Parse    (source string to Lark tree)
        2. Build    (Lark tree to typed AST)
        3. Validate (semantic checks on AST)
        4. Emit     (AST to AgentSpeak strings)

    Args:
        source:   The Regia source code as a string.
        filename: Optional filename for diagnostics (defaults to "<string>").
        emit:     If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    reporter = ErrorReporter()
    reporter.register_source(filename, source)

    # == Stage 1: Parse ========================================================
    try:
        tree = parse(source)
    except (UnexpectedToken, UnexpectedCharacters) as e:
        report_syntax_error(e, reporter, filename=filename)
        return _failure(reporter)

    # == Stage 2: Build AST ====================================================
    builder = ASTBuilder(filename=filename)
    program: Program = builder.transform(tree)

    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 3: Validate =====================================================
    validator = Validator(reporter)
    validator.validate(program)
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 4: Emit AgentSpeak ==============================================
    outputs = {}
    if emit:
        emitter = Emitter()
        outputs = emitter.emit(program)

    return CompileResult(
        success       = True,
        outputs       = outputs,
        error_count   = reporter.error_count,
        warning_count = reporter.warning_count,
        messages      = reporter.messages,
    )


def compile_file(filepath: Union[str, Path], emit: bool = True) -> CompileResult:
    """Compile a single .regia file through the full pipeline.

    Args:
        filepath: Path to the Regia source file.
        emit:     If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    filepath = Path(filepath)
    source   = filepath.read_text(encoding="utf-8")
    return compile_source(source, filename=filepath.name, emit=emit)


def compile_files(filepaths: List[Path], emit: bool = True) -> CompileResult:
    """Compile multiple .regia files through the full pipeline.

    Each file is parsed and built into a Program independently.
    The Programs are then merged into one combined Program for
    validation and emission. File order does not matter.

    Stages:
        1. Parse each file (continue on error to report all failures)
        2. Build AST for each file
        3. Merge all Programs into one
        4. Validate merged Program
        5. Emit AgentSpeak

    Args:
        filepaths: List of paths to Regia source files.
        emit:      If False, skip emission and return empty outputs.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    # Single file: delegate to the simpler path
    if len(filepaths) == 1:
        return compile_file(filepaths[0], emit=emit)

    reporter = ErrorReporter()
    programs: List[Program] = []

    # == Stages 1 & 2: Parse + Build each file =============================
    for fpath in filepaths:
        filename = fpath.name
        source   = fpath.read_text(encoding="utf-8")
        reporter.register_source(filename, source)

        try:
            tree = parse(source)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            report_syntax_error(e, reporter, filename=filename)
            continue  # Try remaining files to report all errors

        builder = ASTBuilder(filename=filename)
        program: Program = builder.transform(tree)
        programs.append(program)

    # If any file failed to parse, stop here
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 3: Merge Programs ===========================================
    merged = Program()
    for prog in programs:
        merged.items.extend(prog.items)

    # == Stage 4: Validate =================================================
    validator = Validator(reporter)
    validator.validate(merged)
    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 5: Emit =====================================================
    outputs = {}
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
    
    This stops after AST building, without validation or emission.
    It prints parsing errors to stdout and exits if there are any,
    otherwise it returns the Program.
    
    Args:
        filepaths: List of paths to Regia source files.
        
    Returns:
        The merged Program AST.
    """
    import sys
    reporter = ErrorReporter()
    programs: List[Program] = []

    for fpath in filepaths:
        filename = fpath.name
        source   = fpath.read_text(encoding="utf-8")
        reporter.register_source(filename, source)

        try:
            tree = parse(source)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            report_syntax_error(e, reporter, filename=filename)
            continue

        builder = ASTBuilder(filename=filename)
        program: Program = builder.transform(tree)
        programs.append(program)

    if reporter.has_errors():
        print(reporter.format_all())
        print(f"\\nParsing failed with {reporter.error_count} error(s).")
        sys.exit(1)

    merged = Program()
    for prog in programs:
        merged.items.extend(prog.items)
    return merged


# == Internal ==================================================================

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
