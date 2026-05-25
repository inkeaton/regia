from dataclasses import dataclass, field
from antlr4      import TerminalNode

from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.generated.RegiaScriptVisitor import RegiaScriptVisitor
from src.errors                       import ErrorReporter


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class StoryInfo:
    name:     str
    priority: int
    line:     int
    doc:      dict = field(default_factory=dict)

@dataclass
class EventInfo:
    name:   str
    origin: str
    line:   int
    doc:    dict = field(default_factory=dict)

@dataclass
class ActionInfo:
    name: str
    line: int
    doc:  dict = field(default_factory=dict)

@dataclass
class ConditionInfo:
    name:   str
    origin: str
    line:   int
    doc:    dict = field(default_factory=dict)


# ── Symbol table ──────────────────────────────────────────────────────────────

@dataclass
class SymbolTable:
    stories:    dict[str, StoryInfo]     = field(default_factory=dict)
    actions:    dict[str, ActionInfo]    = field(default_factory=dict)
    events:     dict[str, EventInfo]     = field(default_factory=dict)
    conditions: dict[str, ConditionInfo] = field(default_factory=dict)


# ── Doc comment parser ────────────────────────────────────────────────────────

def parse_doc_comments(doc_tokens: list) -> dict:
    result = {}
    for token in doc_tokens:
        text   = token.getText()
        at_pos = text.find('@')
        if at_pos == -1:
            continue
        content = text[at_pos + 1:]
        if ':' not in content:
            continue
        key, _, value = content.partition(':')
        result[key.strip().upper()] = value.strip()
    return result


# ── Visitor ───────────────────────────────────────────────────────────────────

class SymbolTableBuilder(RegiaScriptVisitor):
    """
    Pass 1 — collects all declarations into a SymbolTable.
    Reports errors through ErrorReporter.
    """

    def __init__(self, reporter: ErrorReporter):
        self.reporter     = reporter
        self.table        = SymbolTable()
        self._current_doc = {}

    # ── Origin helper ─────────────────────────────────────────────────────────

    def _origin(self, ctx: RegiaScriptParser.OriginContext) -> str:
        return ctx.start.text

    # ── Program ───────────────────────────────────────────────────────────────

    def visitProgram(self, ctx: RegiaScriptParser.ProgramContext):
        for decl in ctx.declaration():
            self.visit(decl)
        return self.table

    # ── Declarations ──────────────────────────────────────────────────────────

    def visitDeclaration(self, ctx: RegiaScriptParser.DeclarationContext):
        self._current_doc = parse_doc_comments(ctx.DOC_COMMENT())
        self.visitChildren(ctx)

    def visitStoryDecl(self, ctx: RegiaScriptParser.StoryDeclContext):
        name     = ctx.ID().getText()
        priority = int(ctx.NUMBER().getText())
        line     = ctx.start.line

        if priority < 1:
            self.reporter.error(
                line, ctx.NUMBER().symbol.column, len(str(priority)),
                f"Story '{name}' has invalid priority '{priority}'.",
                "Priority must be a positive integer (1 or higher)."
            )

        if name in self.table.stories:
            prev = self.table.stories[name].line
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Story '{name}' is declared more than once.",
                f"First declared at line {prev}. Remove one of the declarations."
            )
            return

        self.table.stories[name] = StoryInfo(
            name=name, priority=priority,
            line=line, doc=self._current_doc
        )

    def visitActionDecl(self, ctx: RegiaScriptParser.ActionDeclContext):
        name = ctx.ID().getText()
        line = ctx.start.line

        if name in self.table.actions:
            prev = self.table.actions[name].line
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Action '{name}' is declared more than once.",
                f"First declared at line {prev}. Remove one of the declarations."
            )
            return

        self.table.actions[name] = ActionInfo(
            name=name, line=line, doc=self._current_doc
        )

    def visitEventDecl(self, ctx: RegiaScriptParser.EventDeclContext):
        name   = ctx.ID().getText()
        origin = self._origin(ctx.origin())
        line   = ctx.start.line

        if name in self.table.events:
            prev = self.table.events[name].line
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Event '{name}' is declared more than once.",
                f"First declared at line {prev}. Remove one of the declarations."
            )
            return

        self.table.events[name] = EventInfo(
            name=name, origin=origin,
            line=line, doc=self._current_doc
        )

    def visitConditionDecl(self, ctx: RegiaScriptParser.ConditionDeclContext):
        name   = ctx.ID().getText()
        origin = self._origin(ctx.origin())
        line   = ctx.start.line

        if name in self.table.conditions:
            prev = self.table.conditions[name].line
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Condition '{name}' is declared more than once.",
                f"First declared at line {prev}. Remove one of the declarations."
            )
            return

        self.table.conditions[name] = ConditionInfo(
            name=name, origin=origin,
            line=line, doc=self._current_doc
        )