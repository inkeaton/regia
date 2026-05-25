from dataclasses import dataclass, field
from typing import Optional

from antlr4 import TerminalNode

from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.generated.RegiaScriptVisitor import RegiaScriptVisitor


# Data classes

@dataclass
class StoryInfo:
    name:     str
    priority: int
    doc:      dict = field(default_factory=dict)   # {NAME: ..., MEANING: ...}

@dataclass
class EventInfo:
    name:   str
    origin: str
    doc:    dict = field(default_factory=dict)

@dataclass
class ActionInfo:
    name: str
    doc:  dict = field(default_factory=dict)

@dataclass
class ConditionInfo:
    name:   str
    origin: str
    doc:    dict = field(default_factory=dict)


# Symbol table

@dataclass
class SymbolTable:
    stories:    dict[str, StoryInfo]    = field(default_factory=dict)
    actions:    dict[str, ActionInfo]   = field(default_factory=dict)
    events:     dict[str, EventInfo]    = field(default_factory=dict)
    conditions: dict[str, ConditionInfo]= field(default_factory=dict)


# Helper: parse doc comment lines into a dict

def parse_doc_comments(doc_tokens: list) -> dict:
    """
    Receives a list of DOC_COMMENT token nodes.
    Each line looks like:  # @NAME: The main quest
    Returns: {'NAME': 'The main quest', 'MEANING': '...'}
    """
    result = {}
    for token in doc_tokens:
        text = token.getText()                    # e.g. "# @NAME: The main quest"
        at_pos = text.find('@')
        if at_pos == -1:
            continue
        content = text[at_pos + 1:]              # "NAME: The main quest"
        if ':' not in content:
            continue
        key, _, value = content.partition(':')
        result[key.strip().upper()] = value.strip()
    return result

# Visitor

class SymbolTableBuilder(RegiaScriptVisitor):
    """
    Pass 1 — walks the parse tree and collects all declarations
    into a SymbolTable, reporting any validation errors found.
    """

    def __init__(self):
        self.table  = SymbolTable()
        self.errors = []

    def _error(self, ctx, message: str):
        line = ctx.start.line
        self.errors.append(f"[Line {line}] {message}")

    # Origin helper

    def _origin_text(self, ctx: RegiaScriptParser.OriginContext) -> str:
        """Returns the origin as a plain string: ENVIRONMENT, DIRECTOR, MYSELF"""
        return ctx.start.text

 # Progra

    def visitProgram(self, ctx: RegiaScriptParser.ProgramContext):
        # Visit only declarations — skip duringBlocks in pass 1
        for decl in ctx.declaration():
            self.visit(decl)
        return self.table

    # Declarations

    def visitDeclaration(self, ctx: RegiaScriptParser.DeclarationContext):
        # Collect doc comments attached to this declaration
        doc = parse_doc_comments(ctx.DOC_COMMENT())
        # Visit the concrete declaration, passing the doc dict
        self._current_doc = doc
        self.visitChildren(ctx)

    def visitStoryDecl(self, ctx: RegiaScriptParser.StoryDeclContext):
        name     = ctx.ID().getText()
        priority = int(ctx.NUMBER().getText())
        doc      = getattr(self, '_current_doc', {})

        if name in self.table.stories:
            self._error(ctx, f"Story '{name}' declared more than once.")
            return

        self.table.stories[name] = StoryInfo(
            name=name, priority=priority, doc=doc
        )

    def visitActionDecl(self, ctx: RegiaScriptParser.ActionDeclContext):
        name = ctx.ID().getText()
        doc  = getattr(self, '_current_doc', {})

        if name in self.table.actions:
            self._error(ctx, f"Action '{name}' declared more than once.")
            return

        self.table.actions[name] = ActionInfo(name=name, doc=doc)

    def visitEventDecl(self, ctx: RegiaScriptParser.EventDeclContext):
        name   = ctx.ID().getText()
        origin = self._origin_text(ctx.origin())
        doc    = getattr(self, '_current_doc', {})

        if name in self.table.events:
            self._error(ctx, f"Event '{name}' declared more than once.")
            return

        self.table.events[name] = EventInfo(
            name=name, origin=origin, doc=doc
        )

    def visitConditionDecl(self, ctx: RegiaScriptParser.ConditionDeclContext):
        name   = ctx.ID().getText()
        origin = self._origin_text(ctx.origin())
        doc    = getattr(self, '_current_doc', {})

        if name in self.table.conditions:
            self._error(ctx, f"Condition '{name}' declared more than once.")
            return

        self.table.conditions[name] = ConditionInfo(
            name=name, origin=origin, doc=doc
        )