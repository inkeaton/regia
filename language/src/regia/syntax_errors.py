"""
Syntax error humaniser for the Regia compiler.

Translates Lark exceptions (UnexpectedToken, UnexpectedCharacters) into
user-friendly CompilerMessages with plain-English explanations and hints.
Lark raises structured exceptions with fields like .token, .expected,
.line, .column, which this module converts into our error format.
"""

from typing import Dict, Set

from lark import UnexpectedToken, UnexpectedCharacters

from regia.errors import ErrorReporter


# == Friendly token mapping ====================================================
# Maps Lark terminal names to plain-English descriptions.
# Lark represents anonymous string-literal terminals as their
# quoted form (e.g. the keyword "WHEN" appears as '__ANON_N'),
# but the .expected set on errors uses the human-readable form.
# We map named terminals here; anonymous ones fall through as
# their literal string.

_FRIENDLY: Dict[str, str] = {
    # Named terminals (appear in tree, used in rules)
    "ID":          "a name (e.g. 'run', 'enemy_spotted')",
    "NUMBER":      "an integer number (e.g. '1', '7')",
    "TELL":        "the keyword 'TELL'",
    "BROADCAST":   "the keyword 'BROADCAST'",
    "ACHIEVE":     "the keyword 'ACHIEVE'",
    "BELIEVE":     "the keyword 'BELIEVE'",
    "FORGET":      "the keyword 'FORGET'",
    "PRINT":       "the keyword 'PRINT'",
    "STRING":      "a text string (e.g. \"hello\")",
}


def _friendly_expected(expected: Set[str]) -> str:
    """Convert a set of expected terminal names to a readable string.

    Lark provides the set of terminal names the parser was expecting
    when the error occurred. This function maps them to plain-English.

    Args:
        expected: Set of Lark terminal names (e.g. {"ID", "NUMBER"}).

    Returns:
        A human-readable string like "a name or a whole number".
    """
    friendly = [_FRIENDLY.get(t, f"'{t}'") for t in sorted(expected)]

    if len(friendly) == 1:
        return friendly[0]
    if len(friendly) == 2:
        return f"{friendly[0]} or {friendly[1]}"

    return ", ".join(friendly[:-1]) + f", or {friendly[-1]}"


# == Public API ================================================================

def report_syntax_error(
    error:    UnexpectedToken | UnexpectedCharacters,
    reporter: ErrorReporter,
    filename: str = "",
) -> None:
    """Translate a Lark parse/lex exception into a CompilerMessage.

    Inspects the exception type, extracts position and context
    information, and adds a user-friendly error to the reporter.

    Args:
        error:    The Lark exception (UnexpectedToken or
                  UnexpectedCharacters).
        reporter: The ErrorReporter to add the message to.
        filename: The source file name for multi-file diagnostics.
    """
    if isinstance(error, UnexpectedToken):
        text     = str(error.token) if error.token else "?"
        line     = error.line or 0
        column   = error.column or 0
        length   = len(text) if text != "$END" else 1
        expected = _friendly_expected(error.expected)

        # Lark columns are 1-based; we store 0-based
        reporter.error(
            line, column - 1, length,
            f"Unexpected '{text}' found here.",
            f"Expected {expected}.",
            filename=filename,
        )
        return

    if isinstance(error, UnexpectedCharacters):
        line   = error.line or 0
        column = error.column or 0

        reporter.error(
            line, column - 1, 1,
            "Unrecognised character at this position.",
            "Check for typos or unsupported symbols.",
            filename=filename,
        )
