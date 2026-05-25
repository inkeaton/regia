from dataclasses import dataclass, field

from antlr4 import ParserRuleContext

from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.generated.RegiaScriptVisitor import RegiaScriptVisitor
from src.symbol_table                 import SymbolTable
from src.errors                       import ErrorReporter


@dataclass
class CompiledPlan:
    priority:   int
    agentspeak: str


class AgentSpeakEmitter(RegiaScriptVisitor):

    def __init__(self, table: SymbolTable, reporter: ErrorReporter):
        self.table    = table
        self.reporter = reporter
        self._plans:  list[CompiledPlan] = []

        # Track which symbols are actually used
        self._used_actions:    set[str] = set()
        self._used_events:     set[str] = set()
        self._used_conditions: set[str] = set()

    # ── Result ────────────────────────────────────────────────────────────────

    def get_output(self) -> str:
        sorted_plans = sorted(self._plans, key=lambda p: -p.priority)
        return "\n".join(p.agentspeak for p in sorted_plans)

    def check_unused(self):
        """
        Call after visiting to emit warnings for declared but unused symbols.
        """
        for name, info in self.table.actions.items():
            if name not in self._used_actions:
                self.reporter.warning(
                    info.line, 0, len(name),
                    f"Action '{name}' is declared but never used.",
                    "Remove it, or add a plan that calls it."
                )
        for name, info in self.table.events.items():
            if name not in self._used_events:
                self.reporter.warning(
                    info.line, 0, len(name),
                    f"Event '{name}' is declared but never used in any WHEN block.",
                    "Remove it, or add a WHEN block that reacts to it."
                )
        for name, info in self.table.conditions.items():
            if name not in self._used_conditions:
                self.reporter.warning(
                    info.line, 0, len(name),
                    f"Condition '{name}' is declared but never used.",
                    "Remove it, or use it in an IF clause or DO BELIEVE/FORGET."
                )

    # ── Program ───────────────────────────────────────────────────────────────

    def visitProgram(self, ctx: RegiaScriptParser.ProgramContext):
        for block in ctx.duringBlock():
            self.visit(block)

    # ── During block ──────────────────────────────────────────────────────────

    def visitDuringBlock(self, ctx: RegiaScriptParser.DuringBlockContext):
        story_ref = ctx.storyRef()

        if story_ref.ALWAYS():
            story_name = None
            priority   = 0
        else:
            story_name = story_ref.ID().getText()
            if story_name not in self.table.stories:
                self.reporter.error(
                    ctx.start.line,
                    story_ref.start.column,
                    len(story_name),
                    f"Story '{story_name}' is not declared.",
                    f"Add 'STORY {story_name} PRIORITY <n>.' to the declarations."
                )
                return
            priority = self.table.stories[story_name].priority

        for when in ctx.whenBlock():
            plan = self._emit_when(when, story_name, priority)
            if plan is not None:
                self._plans.append(CompiledPlan(
                    priority=priority,
                    agentspeak=plan
                ))

    # ── When block ────────────────────────────────────────────────────────────

    def _emit_when(
        self,
        ctx:        RegiaScriptParser.WhenBlockContext,
        story_name: str | None,
        priority:   int
    ) -> str | None:

        event_name = ctx.ID().getText()
        origin     = ctx.origin().start.text

        if event_name not in self.table.events:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(event_name),
                f"Event '{event_name}' is not declared.",
                f"Add 'EVENT {event_name} {origin}.' to the declarations."
            )
            return None

        declared_event = self.table.events[event_name]
        if declared_event.origin != origin:
            self.reporter.error(
                ctx.start.line,
                ctx.origin().start.column,
                len(origin),
                f"Event '{event_name}' is declared as "
                f"{declared_event.origin} but used here as {origin}.",
                f"Change the origin here to {declared_event.origin}."
            )
            return None

        self._used_events.add(event_name)

        # ── Trigger ───────────────────────────────────────────────────────────
        trigger = self._emit_trigger(event_name, origin)

        # ── Context ───────────────────────────────────────────────────────────
        context_parts = []
        if story_name is not None:
            context_parts.append(f"story({story_name}, {priority})")

        if ctx.IF():
            cond = self._emit_condExpr(ctx.condExpr())
            if cond is None:
                return None
            if story_name is not None and len(ctx.condExpr().condAnd()) > 1:
                cond = f"({cond})"
            context_parts.append(cond)

        context = " & ".join(context_parts) if context_parts else "true"

        # ── Body ──────────────────────────────────────────────────────────────
        body = self._emit_doSequence(ctx.doSequence())
        if body is None:
            return None

        return f"{trigger} : {context} <- {body}."

    # ── Trigger ───────────────────────────────────────────────────────────────

    def _emit_trigger(self, name: str, origin: str) -> str:
        if origin == "ENVIRONMENT":
            return f"+{name}[source(percept)]"
        elif origin == "DIRECTOR":
            return f"+{name}[source(director)]"
        return f"+{name}"

    # ── Condition expression ──────────────────────────────────────────────────

    def _emit_condExpr(
        self, ctx: RegiaScriptParser.CondExprContext
    ) -> str | None:
        ands = ctx.condAnd()
        if len(ands) == 1:
            return self._emit_condAnd(ands[0], wrap=False)
        parts = [self._emit_condAnd(a, wrap=True) for a in ands]
        if any(p is None for p in parts):
            return None
        return " | ".join(parts)

    def _emit_condAnd(
        self,
        ctx:  RegiaScriptParser.CondAndContext,
        wrap: bool = False
    ) -> str | None:
        parts = []
        for term in ctx.condTerm():
            t = self._emit_condTerm(term)
            if t is None:
                return None
            parts.append(t)
        if len(parts) == 1:
            return parts[0]
        result = " & ".join(parts)
        return f"({result})" if wrap else result

    def _emit_condTerm(
        self, ctx: RegiaScriptParser.CondTermContext
    ) -> str | None:
        atom = self._emit_condAtom(ctx.condAtom())
        if atom is None:
            return None
        return f"~{atom}" if ctx.NOT() else atom

    def _emit_condAtom(
        self, ctx: RegiaScriptParser.CondAtomContext
    ) -> str | None:
        if ctx.LPAREN():
            inner = self._emit_condExpr(ctx.condExpr())
            if inner is None:
                return None
            return f"({inner})"

        name   = ctx.ID().getText()
        origin = ctx.origin().start.text

        if name not in self.table.conditions:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(name),
                f"Condition '{name}' is not declared.",
                f"Add 'CONDITION {name} {origin}.' to the declarations."
            )
            return None

        declared = self.table.conditions[name]
        if declared.origin != origin:
            self.reporter.error(
                ctx.start.line,
                ctx.origin().start.column,
                len(origin),
                f"Condition '{name}' is declared as "
                f"{declared.origin} but used here as {origin}.",
                f"Change the origin here to {declared.origin}."
            )
            return None

        self._used_conditions.add(name)
        return name

    # ── Do sequence ───────────────────────────────────────────────────────────

    def _emit_doSequence(
        self, ctx: RegiaScriptParser.DoSequenceContext
    ) -> str | None:
        parts = []
        for action in ctx.doAction():
            a = self._emit_doAction(action)
            if a is None:
                return None
            parts.append(a)
        return "; ".join(parts)

    def _emit_doAction(
        self, ctx: RegiaScriptParser.DoActionContext
    ) -> str | None:

        if ctx.BELIEVE():
            name = ctx.ID().getText()
            if name not in self.table.conditions:
                self.reporter.error(
                    ctx.start.line,
                    ctx.ID().symbol.column,
                    len(name),
                    f"Condition '{name}' is not declared.",
                    f"Add 'CONDITION {name} MYSELF.' to the declarations."
                )
                return None
            self._used_conditions.add(name)
            return f"+{name}"

        if ctx.FORGET():
            name = ctx.ID().getText()
            if name not in self.table.conditions:
                self.reporter.error(
                    ctx.start.line,
                    ctx.ID().symbol.column,
                    len(name),
                    f"Condition '{name}' is not declared.",
                    f"Add 'CONDITION {name} MYSELF.' to the declarations."
                )
                return None
            self._used_conditions.add(name)
            return f"-{name}"

        name = ctx.ID().getText()
        if name not in self.table.actions:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(name),
                f"Action '{name}' is not declared.",
                f"Add 'ACTION {name}.' to the declarations."
            )
            return None
        self._used_actions.add(name)
        return name