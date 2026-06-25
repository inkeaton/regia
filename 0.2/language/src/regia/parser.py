"""
Parser module for the Regia compiler.

Loads the Lark grammar at import time and provides the parse()
entry point. This module is the only place that interacts with
Lark directly. It produces a lark.Tree (concrete syntax tree)
which is then transformed into our own AST by the ast_builder module.
"""

from pathlib import Path

from lark import Lark, Tree, UnexpectedToken, UnexpectedCharacters


# == Grammar loading ===========================================================
# The grammar file lives alongside this module in the package.
# It is loaded once at import time; Lark compiles it into an LALR
# table internally (fast, no external tools needed).

_GRAMMAR_PATH: Path = Path(__file__).parent / "grammars" / "regia.lark"

_parser: Lark = Lark(
    _GRAMMAR_PATH.read_text(encoding="utf-8"),
    parser="lalr",
    start="program",
    propagate_positions=True,  # Attach line/col to every Tree node
)


# == Public API ================================================================

def parse(source: str) -> Tree:
    """Parse a Regia source string into a Lark parse tree.

    Args:
        source: The Regia source code as a string.

    Returns:
        A Lark Tree representing the concrete parse tree.

    Raises:
        UnexpectedToken:      On syntax errors (wrong token).
        UnexpectedCharacters: On lexer errors  (unrecognised character).
    """
    return _parser.parse(source)
