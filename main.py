import sys
from antlr4 import CommonTokenStream, FileStream

from src.generated.RegiaScriptLexer   import RegiaScriptLexer
from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.symbol_table                 import SymbolTableBuilder

def parse(filepath: str):
    input_stream = FileStream(filepath, encoding="utf-8")
    lexer        = RegiaScriptLexer(input_stream)
    stream       = CommonTokenStream(lexer)
    parser       = RegiaScriptParser(stream)
    tree         = parser.program()

    # Syntax errors
    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"[ERROR] {parser.getNumberOfSyntaxErrors()} syntax error(s).")
        sys.exit(1)

    # Pass 1 — build symbol table
    builder = SymbolTableBuilder()
    table   = builder.visit(tree)

    if builder.errors:
        for e in builder.errors:
            print(e)
        sys.exit(1)

    # Print what we found
    print("[OK] Symbol table built successfully.\n")
    print("=== STORIES ===")
    for s in table.stories.values():
        print(f"  {s.name} (priority {s.priority}) doc={s.doc}")
    print("\n=== ACTIONS ===")
    for a in table.actions.values():
        print(f"  {a.name} doc={a.doc}")
    print("\n=== EVENTS ===")
    for e in table.events.values():
        print(f"  {e.name} [{e.origin}] doc={e.doc}")
    print("\n=== CONDITIONS ===")
    for c in table.conditions.values():
        print(f"  {c.name} [{c.origin}] doc={c.doc}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-file>")
        sys.exit(1)
    parse(sys.argv[1])