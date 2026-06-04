from dataclasses import dataclass, field
from pathlib     import Path
from antlr4      import CommonTokenStream, FileStream

from src.generated.RegiaScriptLexer   import RegiaScriptLexer
from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.errors                       import ErrorReporter, CompilerMessage
from src.antlr_error_listener         import RegiaScriptErrorListener
from src.symbol_table                 import SymbolTableBuilder
from src.emitter                      import AgentSpeakEmitter


# == Result type ===============================================================

@dataclass
class CompileResult:
    success:       bool
    outputs:       dict[str, str]          # agent_name → AgentSpeak string
    error_count:   int
    warning_count: int
    messages:      list[CompilerMessage]


# == Core compile function =====================================================

def compile_file(filepath: str | Path) -> CompileResult:
    filepath = Path(filepath)
    source   = filepath.read_text(encoding="utf-8")
    reporter = ErrorReporter(source)

    # == Parse =================================================================
    input_stream = FileStream(str(filepath), encoding="utf-8")
    lexer        = RegiaScriptLexer(input_stream)
    stream       = CommonTokenStream(lexer)
    parser       = RegiaScriptParser(stream)

    lexer.removeErrorListeners()
    lexer.addErrorListener(RegiaScriptErrorListener(reporter))
    parser.removeErrorListeners()
    parser.addErrorListener(RegiaScriptErrorListener(reporter))

    tree = parser.program()

    if reporter.has_errors():
        return _failure(reporter)

    # == Pass 1 - Symbol table =================================================
    builder = SymbolTableBuilder(reporter)
    table   = builder.visit(tree)

    if reporter.has_errors():
        return _failure(reporter)

    # == Pass 2 - Emit AgentSpeak ==============================================
    emitter = AgentSpeakEmitter(table, reporter)
    emitter.visit(tree)
    emitter.check_unused()

    if reporter.has_errors():
        return _failure(reporter)

    return CompileResult(
        success       = True,
        outputs       = emitter.get_outputs(),
        error_count   = reporter.error_count(),
        warning_count = reporter.warning_count(),
        messages      = reporter._messages,
    )


def _failure(reporter: ErrorReporter) -> CompileResult:
    return CompileResult(
        success       = False,
        outputs       = {},
        error_count   = reporter.error_count(),
        warning_count = reporter.warning_count(),
        messages      = reporter._messages,
    )