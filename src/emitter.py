from dataclasses import dataclass, field
from antlr4      import ParserRuleContext

from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.generated.RegiaScriptVisitor import RegiaScriptVisitor
from src.symbol_table                 import (
    SymbolTable, StoryInfo, AgentInfo,
    ActionInfo, EventInfo, ConditionInfo, PhaseInfo
)
from src.errors import ErrorReporter


# == Compiled plan =============================================================

@dataclass
class CompiledPlan:
    priority:   int
    agentspeak: str


# == Per-agent output buffer ===================================================

@dataclass
class AgentBuffer:
    name:             str
    plans:            list[CompiledPlan] = field(default_factory=list)
    initial_beliefs:  list[str]          = field(default_factory=list)
    transition_plans: list[str]          = field(default_factory=list)

    def get_output(self) -> str:
        """
        The get_output method merges the initial beliefs, transition plans, and regular plans
        into a single AgentSpeak program string, with sections separated by comments.
        """
        sorted_plans = sorted(self.plans, key=lambda p: -p.priority)
        parts = []

        if self.initial_beliefs:
            parts.append("// == Initial beliefs " + "=" * 40)
            for b in self.initial_beliefs:
                parts.append(f"{b}.")
            parts.append("")

        if self.transition_plans:
            parts.append("// == Atomic state transition plans " + "=" * 26)
            for t in self.transition_plans:
                parts.append(t)
            parts.append("")

        if sorted_plans:
            parts.append("// == Plans " + "=" * 49)
            for p in sorted_plans:
                parts.append(p.agentspeak)

        return "\n".join(parts)


# == Emitter ===================================================================

class AgentSpeakEmitter(RegiaScriptVisitor):
    """
    Pass 2: walks the parse tree story by story, agent by agent,
    validates all references, and emits AgentSpeak plan strings.
    Produces one AgentBuffer per unique agent name across all stories.
    """

    def __init__(self, table: SymbolTable, reporter: ErrorReporter):
        self.table    = table
        self.reporter = reporter

        # One buffer per agent name, merged across all stories
        self._buffers: dict[str, AgentBuffer] = {}

        # Current compilation context
        self._current_story: StoryInfo | None = None
        self._current_agent: AgentInfo | None = None

        # Unused symbol tracking
        self._used_actions:    set[str] = set()
        self._used_events:     set[str] = set()
        self._used_conditions: set[str] = set()

    # == Public interface ======================================================

    def get_outputs(self) -> dict[str, str]:
        return {
            name: buf.get_output()
            for name, buf in self._buffers.items()
        }

    def check_unused(self):
        """
        Warn about declared symbols never referenced in any plan.
        """
        for story in self.table.stories.values():
            for name, info in story.actions.items():
                if name not in self._used_actions:
                    self.reporter.warning(
                        info.line, 0, len(name),
                        f"Action '{name}' is declared in story "
                        f"'{story.name}' but never used.",
                        "Remove it, or add a DO action that calls it."
                    )
            for name, info in story.events.items():
                if name not in self._used_events:
                    self.reporter.warning(
                        info.line, 0, len(name),
                        f"Event '{name}' is declared in story "
                        f"'{story.name}' but never used.",
                        "Remove it, or add a WHEN block that reacts to it."
                    )
            for name, info in story.conditions.items():
                if name not in self._used_conditions:
                    self.reporter.warning(
                        info.line, 0, len(name),
                        f"Condition '{name}' is declared in story "
                        f"'{story.name}' but never used.",
                        "Remove it, or use it in an IF clause or "
                        "DO BELIEVE/FORGET."
                    )
            for agent in story.agents.values():
                for name, info in agent.actions.items():
                    if name not in self._used_actions:
                        self.reporter.warning(
                            info.line, 0, len(name),
                            f"Action '{name}' is declared for agent "
                            f"'{agent.name}' in story '{story.name}' "
                            f"but never used.",
                            "Remove it, or add a DO action that calls it."
                        )

    # == Helpers ===============================================================

    def _get_buffer(self, agent_name: str) -> AgentBuffer:
        if agent_name not in self._buffers:
            self._buffers[agent_name] = AgentBuffer(name=agent_name)
        return self._buffers[agent_name]

    def _effective_actions(self) -> dict:
        """Agent-local actions merged with story-level actions."""
        merged = dict(self._current_story.actions) if self._current_story else {}
        if self._current_agent:
            merged.update(self._current_agent.actions)
        return merged

    def _effective_events(self) -> dict:
        merged = dict(self._current_story.events) if self._current_story else {}
        if self._current_agent:
            merged.update(self._current_agent.events)
        return merged

    def _effective_conditions(self) -> dict:
        merged = dict(self._current_story.conditions) \
            if self._current_story else {}
        if self._current_agent:
            merged.update(self._current_agent.conditions)
        return merged

    def _effective_phases(self) -> dict:
        if self._current_story:
            return self._current_story.phases
        return {}

    def _error(
        self,
        ctx:     ParserRuleContext,
        message: str,
        hint:    str = ""
    ):
        self.reporter.error(
            ctx.start.line,
            ctx.start.column,
            len(ctx.start.text),
            message,
            hint
        )

    # == Program ===============================================================

    def visitProgram(self, ctx: RegiaScriptParser.ProgramContext):
        for story_def in ctx.storyDef():
            self.visit(story_def)

    # == Story definitions =====================================================

    def visitStoryDef(self, ctx: RegiaScriptParser.StoryDefContext):
        self.visitChildren(ctx)

    def visitDefaultStory(
        self, ctx: RegiaScriptParser.DefaultStoryContext
    ):
        story = self.table.stories.get("DEFAULT")
        if story is None:
            return

        self._current_story = story

        for agent_block in ctx.agentBlock():
            self._emit_agent_block(agent_block, story)

        self._current_story = None

    def visitNamedStory(
        self, ctx: RegiaScriptParser.NamedStoryContext
    ):
        story_name = ctx.ID().getText()
        story      = self.table.stories.get(story_name)
        if story is None:
            return

        self._current_story = story

        for agent_block in ctx.agentBlock():
            self._emit_agent_block(agent_block, story)

        self._current_story = None

    # == Agent block ===========================================================

    def _emit_agent_block(
        self,
        ctx:   RegiaScriptParser.AgentBlockContext,
        story: StoryInfo
    ):
        agent_name = ctx.ID().getText()
        agent      = story.agents.get(agent_name)
        if agent is None:
            return

        buffer = self._get_buffer(agent_name)
        self._current_agent = agent

        # Emit initial phase belief for named stories
        if not story.is_default and story.phases:
            for phase in story.phases.values():
                if phase.initial:
                    if phase.name not in buffer.initial_beliefs:
                        buffer.initial_beliefs.append(phase.name)
                    break

            # Generate @atomic transition plans for this story's phases
            all_phases = list(story.phases.keys())
            # Generate reception handlers with guard to prevent double-update
            # Generate @atomic transition plans (for when this agent triggers a transition)
        all_phases = list(story.phases.keys())
        for phase_name in all_phases:
            goal_name = f"enter_{story.name}_{phase_name}"
            removals  = "; ".join(
                f"-{p}" for p in all_phases if p != phase_name
            )
            addition  = f"+{phase_name}"
            body      = f"{removals}; {addition}" if removals else addition
            broadcast = f".broadcast(tell, {goal_name})"
            plan      = (
                f"@atomic\n"
                f"+!{goal_name}\n"
                f"    <- {body}; {broadcast}."
            )
            buffer.transition_plans.append(plan)

        # Generate reception handlers (for when another agent broadcasts a transition)
        # Guard 'not phaseName' prevents double-update if agent receives own broadcast
        for phase_name in all_phases:
            goal_name = f"enter_{story.name}_{phase_name}"
            removals  = "; ".join(
                f"-{p}" for p in all_phases if p != phase_name
            )
            addition  = f"+{phase_name}"
            body      = f"{removals}; {addition}" if removals else addition
            handler   = (
                f"+{goal_name}[source(percept)] : not {phase_name}\n"
                f"    <- {body}."
            )
            buffer.transition_plans.append(handler)

        # Walk during blocks
        for section in ctx.agentSection():
            if section.duringBlock():
                self._emit_during_block(
                    section.duringBlock(), story, buffer
                )

        self._current_agent = None

    # == During block ==========================================================

    def _emit_during_block(
        self,
        ctx:    RegiaScriptParser.DuringBlockContext,
        story:  StoryInfo,
        buffer: AgentBuffer
    ):
        phase_ref  = ctx.phaseRef()
        is_always  = bool(phase_ref.ALWAYS())
        phase_name = None if is_always else phase_ref.ID().getText()

        # Priority: named story priority, or 0 for DEFAULT
        priority = story.priority if not story.is_default else 0

        for when in ctx.whenBlock():
            plan = self._emit_when(
                when, story, phase_name, priority
            )
            if plan is not None:
                buffer.plans.append(CompiledPlan(
                    priority=priority,
                    agentspeak=plan
                ))

    # == When block ============================================================

    def _emit_when(
        self,
        ctx:        RegiaScriptParser.WhenBlockContext,
        story:      StoryInfo,
        phase_name: str | None,
        priority:   int
    ) -> str | None:

        event_name = ctx.ID().getText()
        origin     = ctx.origin().start.text
        events     = self._effective_events()

        # Validate event reference
        if event_name not in events:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(event_name),
                f"Event '{event_name}' is not declared.",
                f"Add 'EVENT {event_name} {origin}.' to the story "
                f"or agent declarations."
            )
            return None

        declared_event = events[event_name]
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

        # == Trigger ===========================================================
        trigger = self._emit_trigger(event_name, origin)

        # == Context ===========================================================
        context_parts = []

        # Story conjunct - named stories only
        if not story.is_default:
            context_parts.append(
                f"story({story.name}, {story.priority})"
            )

        # Phase conjunct - DURING phaseName only, not DURING ALWAYS
        if phase_name is not None:
            context_parts.append(phase_name)

        # IF clause
        if ctx.IF():
            cond = self._emit_condExpr(ctx.condExpr())
            if cond is None:
                return None
            # Wrap top-level OR when joined with preceding context
            if context_parts and len(ctx.condExpr().condAnd()) > 1:
                cond = f"({cond})"
            context_parts.append(cond)

        context = " & ".join(context_parts) if context_parts else "true"

        # == Body ==============================================================
        body = self._emit_doSequence(ctx.doSequence(), story)
        if body is None:
            return None

        return f"{trigger} : {context} <- {body}."

    # == Trigger ===============================================================

    def _emit_trigger(self, name: str, origin: str) -> str:
        mapping = {
            "ENVIRONMENT": f"+{name}[source(percept)]",
            "DIRECTOR":    f"+{name}[source(director)]",
            "PLAYER":      f"+{name}[source(player)]",
            "TIMER":       f"+{name}[source(timer)]",
        }
        return mapping.get(origin, f"+{name}")

    # == Condition expression ==================================================

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

        name       = ctx.ID().getText()
        origin     = ctx.origin().start.text
        conditions = self._effective_conditions()

        if name not in conditions:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(name),
                f"Condition '{name}' is not declared.",
                f"Add 'CONDITION {name} {origin}.' to the story "
                f"or agent declarations."
            )
            return None

        declared = conditions[name]
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

    # == Do sequence ===========================================================

    def _emit_doSequence(
        self,
        ctx:   RegiaScriptParser.DoSequenceContext,
        story: StoryInfo
    ) -> str | None:
        parts = []
        for action in ctx.doAction():
            a = self._emit_doAction(action, story)
            if a is None:
                return None
            parts.append(a)
        return "; ".join(parts)

    def _emit_doAction(
        self,
        ctx:   RegiaScriptParser.DoActionContext,
        story: StoryInfo
    ) -> str | None:

        # DO BELIEVE
        if ctx.BELIEVE():
            name       = ctx.ID().getText()
            conditions = self._effective_conditions()
            if name not in conditions:
                self.reporter.error(
                    ctx.start.line,
                    ctx.ID().symbol.column,
                    len(name),
                    f"Condition '{name}' is not declared.",
                    "Add the CONDITION declaration to the story "
                    "or agent block."
                )
                return None
            self._used_conditions.add(name)
            return f"+{name}"

        # DO FORGET
        if ctx.FORGET():
            name       = ctx.ID().getText()
            conditions = self._effective_conditions()
            if name not in conditions:
                self.reporter.error(
                    ctx.start.line,
                    ctx.ID().symbol.column,
                    len(name),
                    f"Condition '{name}' is not declared.",
                    "Add the CONDITION declaration to the story "
                    "or agent block."
                )
                return None
            self._used_conditions.add(name)
            return f"-{name}"

        # ENTER phase
        if ctx.ENTER():
            name   = ctx.ID().getText()
            phases = self._effective_phases()
            if name not in phases:
                self.reporter.error(
                    ctx.start.line,
                    ctx.ID().symbol.column,
                    len(name),
                    f"Phase '{name}' is not declared in story "
                    f"'{story.name}'.",
                    f"Add 'PHASE {name}.' to the story declarations."
                )
                return None
            goal = f"enter_{story.name}_{name}"
            return f"!{goal}"

        # DO action
        name    = ctx.ID().getText()
        actions = self._effective_actions()
        if name not in actions:
            self.reporter.error(
                ctx.start.line,
                ctx.ID().symbol.column,
                len(name),
                f"Action '{name}' is not declared.",
                "Add the ACTION declaration to the story "
                "or agent block."
            )
            return None
        self._used_actions.add(name)
        return name