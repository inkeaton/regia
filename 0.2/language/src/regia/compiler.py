"""
Compiler pipeline for the Regia compiler.

Orchestrates parsing, AST building, validation, and emission.
Each stage only runs if the previous produced zero errors.
This module contains no grammar or emission logic; it is pure wiring.
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


# == Result type ===============================================================

@dataclass
class CompileResult:
    """The result of compiling a Regia source file.

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

def compile_source(source: str, filename: str = "<string>") -> CompileResult:
    """Compile a Regia source string through the full pipeline.

    Stages:
        1. Parse    (source string to Lark tree)
        2. Build    (Lark tree to typed AST)
        3. Validate (semantic checks on AST)       [TODO]
        4. Emit     (AST to AgentSpeak strings)     [TODO]

    Args:
        source:   The Regia source code as a string.
        filename: Optional filename for diagnostics (defaults to "<string>").

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    reporter = ErrorReporter(source)

    # == Stage 1: Parse ========================================================
    try:
        tree = parse(source)
    except (UnexpectedToken, UnexpectedCharacters) as e:
        report_syntax_error(e, reporter)
        return _failure(reporter)

    # == Stage 2: Build AST ====================================================
    builder = ASTBuilder()
    program: Program = builder.transform(tree)

    if reporter.has_errors():
        return _failure(reporter)

    # == Stage 3: Validate =====================================================
    # TODO: symbol table validation pass
    # validator = Validator(reporter)
    # validator.validate(program)
    # if reporter.has_errors():
    #     return _failure(reporter)

    # == Stage 4: Emit AgentSpeak ==============================================
    # TODO: emission pass
    # emitter = Emitter(reporter)
    # outputs = emitter.emit(program)

    return CompileResult(
        success       = True,
        outputs       = {},         # placeholder until emission is implemented
        error_count   = reporter.error_count,
        warning_count = reporter.warning_count,
        messages      = reporter.messages,
    )


def compile_file(filepath: Union[str, Path]) -> CompileResult:
    """Compile a .rgs file through the full pipeline.

    Args:
        filepath: Path to the Regia source file.

    Returns:
        A CompileResult with success status, outputs, and diagnostics.
    """
    filepath = Path(filepath)
    source   = filepath.read_text(encoding="utf-8")
    return compile_source(source, filename=filepath.name)


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
