from dataclasses import dataclass, field

from src.generated.RegiaScriptParser  import RegiaScriptParser
from src.generated.RegiaScriptVisitor import RegiaScriptVisitor
from src.errors                       import ErrorReporter

# the symbol table is built in the first pass of the compiler, and contains all 
# the information about declared stories, agents, actions, events, conditions, and phases.
# it is used in later passes for semantic analysis and code generation, and also 
# for error reporting (e.g. to show where a symbol was first declared when reporting duplicates).

# == Data classes ==============================================================

@dataclass
class ActionInfo:
    name: str
    line: int
    doc:  dict = field(default_factory=dict)

@dataclass
class EventInfo:
    name:   str
    origin: str
    line:   int
    doc:    dict = field(default_factory=dict)

@dataclass
class ConditionInfo:
    name:   str
    origin: str
    line:   int
    doc:    dict = field(default_factory=dict)

@dataclass
class PhaseInfo:
    name:    str
    line:    int
    initial: bool = False
    doc:     dict = field(default_factory=dict)

@dataclass
class AgentInfo:
    name:       str
    line:       int
    is_player:  bool                     = False
    actions:    dict[str, ActionInfo]    = field(default_factory=dict)
    events:     dict[str, EventInfo]     = field(default_factory=dict)
    conditions: dict[str, ConditionInfo] = field(default_factory=dict)
    doc:        dict                     = field(default_factory=dict)            

@dataclass
class TransitionInfo:
    from_phase:    str
    to_phase:      str | None
    is_terminal:   bool
    event_name:    str
    event_origin:  str
    cond_ctx:      object | None   # RegiaScriptParser.CondExprContext or None
    line:          int

@dataclass
class StoryInfo:
    name:       str
    priority:   int | None              # None for DEFAULT story
    line:       int
    is_default: bool                    = False
    actions:    dict[str, ActionInfo]   = field(default_factory=dict)
    events:     dict[str, EventInfo]    = field(default_factory=dict)
    conditions: dict[str, ConditionInfo]= field(default_factory=dict)
    phases:     dict[str, PhaseInfo]    = field(default_factory=dict)
    agents:     dict[str, AgentInfo]    = field(default_factory=dict)
    doc:        dict                    = field(default_factory=dict)
    transitions: list[TransitionInfo] = field(default_factory=list)
    participants: dict[str, list[str]] = field(default_factory=dict)
    agent_names: list[str]              = field(default_factory=list)


# == Symbol table ==============================================================

@dataclass
class SymbolTable:
    stories: dict[str, StoryInfo] = field(default_factory=dict)


# == Doc comment parser ========================================================

# Parses documentation comments and extracts key-value pairs.
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


# == Registration helpers ======================================================

def _origin(ctx: RegiaScriptParser.OriginContext) -> str:
    return ctx.start.text


def _check_duplicate(
    name: str, entity_type: str, ctx, registry: dict, reporter: ErrorReporter,
    msg_suffix: str = "", suggestion: str = None
) -> bool:
    if name in registry:
        prev_line = registry[name].line
        sugg = suggestion if suggestion is not None else (
            f"First declared at line {prev_line}. "
            f"Remove one of the declarations."
        )
        msg_verb = "appears" if entity_type == "Agent" else "is declared"
        
        reporter.error(
            ctx.start.line, ctx.ID().symbol.column, len(name),
            f"{entity_type} '{name}' {msg_verb} more than once{msg_suffix}.",
            sugg
        )
        return True
    return False


def _register_action(ctx, registry: dict, reporter: ErrorReporter, doc: dict):
    name = ctx.ID().getText()
    line = ctx.start.line

    if _check_duplicate(name, "Action", ctx, registry, reporter):
        return
    
    registry[name] = ActionInfo(name=name, line=line, doc=doc)


def _register_event(ctx, registry: dict, reporter: ErrorReporter, doc: dict):
    name   = ctx.ID().getText()
    origin = _origin(ctx.origin())
    line   = ctx.start.line

    if _check_duplicate(name, "Event", ctx, registry, reporter):
        return
    
    registry[name] = EventInfo(name=name, origin=origin, line=line, doc=doc)


def _register_condition(
    ctx, registry: dict, reporter: ErrorReporter, doc: dict
):
    name   = ctx.ID().getText()
    origin = _origin(ctx.origin())
    line   = ctx.start.line

    if _check_duplicate(name, "Condition", ctx, registry, reporter):
        return
    
    registry[name] = ConditionInfo(
        name=name, origin=origin, line=line, doc=doc
    )


# == Visitor ===================================================================

class SymbolTableBuilder(RegiaScriptVisitor):
    """
    Pass 1: walks the parse tree and builds a SymbolTable.
    Handles default stories, named stories, story-level declarations,
    phases, and per-agent declarations.
    """

    def __init__(self, reporter: ErrorReporter):
        self.reporter = reporter
        self.table    = SymbolTable()

    # == Program ===============================================================

    def visitProgram(self, ctx: RegiaScriptParser.ProgramContext):
        for story_def in ctx.storyDef():
            self.visit(story_def)
        return self.table

    # == Story definitions =====================================================

    def visitStoryDef(self, ctx: RegiaScriptParser.StoryDefContext):
        self.visitChildren(ctx)

    def visitDefaultStory(self, ctx: RegiaScriptParser.DefaultStoryContext):
        doc  = parse_doc_comments(ctx.DOC_COMMENT())
        name = "DEFAULT"
        line = ctx.start.line

        if name in self.table.stories:
            self.reporter.error(
                line, 0, len(name),
                "Only one DEFAULT story is allowed per file.",
                "Merge all default agent behaviour into one STORY DEFAULT block."
            )
            return

        story = StoryInfo(
            name=name, priority=None, line=line, is_default=True, doc=doc
        )
        self.table.stories[name] = story

        for agent_block in ctx.agentBlock():
            self._visit_agent_block(agent_block, story)

    def visitNamedStory(self, ctx: RegiaScriptParser.NamedStoryContext):
        doc      = parse_doc_comments(ctx.DOC_COMMENT())
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

        story = StoryInfo(
            name=name, priority=priority, line=line, is_default=False, doc=doc
        )
        self.table.stories[name] = story

        # Story-level declarations
        for decl in ctx.declaration():
            self._visit_story_declaration(decl, story)

        # Phase declarations — INITIAL keyword marks the initial phase
        initial_seen = False
        for phase_ctx in ctx.phaseDecl():
            phase_doc  = parse_doc_comments(phase_ctx.DOC_COMMENT())
            phase_name = phase_ctx.ID().getText()
            phase_line = phase_ctx.start.line
            has_initial = bool(phase_ctx.INITIAL())

            if phase_name in story.phases:
                self.reporter.error(
                    phase_line, phase_ctx.ID().symbol.column, len(phase_name),
                    f"Phase '{phase_name}' is declared more than once in story '{name}'.",
                    "Remove one of the PHASE declarations."
                )
                continue

            if has_initial:
                if initial_seen:
                    self.reporter.error(
                        phase_line, phase_ctx.ID().symbol.column, len(phase_name),
                        f"Phase '{phase_name}' is marked INITIAL but another phase "
                        f"is already the initial phase.",
                        "Only one phase per story can be marked INITIAL."
                    )
                initial_seen = True

            story.phases[phase_name] = PhaseInfo(
                name=phase_name,
                line=phase_line,
                initial=has_initial,
                doc=phase_doc
            )

        if story.phases and not initial_seen:
            self.reporter.error(
                line, 0, len(name),
                f"Story '{name}' has phases but none is marked INITIAL.",
                "Add INITIAL after the starting phase name: 'PHASE asking INITIAL.'"
            )

        # Story-level agent declarations
        for agent_decl in ctx.storyAgentDecl():
            agent_doc  = parse_doc_comments(agent_decl.DOC_COMMENT())
            agent_name = agent_decl.ID().getText()
            agent_line = agent_decl.start.line
            is_player  = bool(agent_decl.PLAYER())

            if agent_name in story.agents:
                self.reporter.error(
                    agent_line, agent_decl.ID().symbol.column, len(agent_name),
                    f"Agent '{agent_name}' is declared more than once in story '{name}'.",
                    "Remove one of the AGENT declarations."
                )
                continue

            agent = AgentInfo(
                name=agent_name, line=agent_line, is_player=is_player, doc=agent_doc
            )
            story.agents[agent_name] = agent
            story.agent_names.append(agent_name)

        # During blocks
        for during in ctx.duringBlock():
            self._visit_during_block(during, story)
    
    def _visit_during_block(self, ctx, story):
        phase_ref = ctx.phaseRef()
        is_story  = bool(phase_ref.STORY())
        phase_name = None if is_story else phase_ref.ID().getText()

        # Validate TRANSITION rules not allowed in DURING STORY
        if is_story and ctx.transitionRule():
            for rule in ctx.transitionRule():
                self.reporter.error(
                    rule.start.line, rule.start.column, len("TRANSITION"),
                    "TRANSITION rules are not allowed in DURING STORY.",
                    "Move this transition into a named phase block."
                )

        if not is_story and phase_name not in story.phases:
            self.reporter.error(
                ctx.start.line, phase_ref.start.column, len(phase_name),
                f"Phase '{phase_name}' is not declared in story '{story.name}'.",
                f"Add 'PHASE {phase_name} INITIAL.' or 'PHASE {phase_name}.' "
                f"to the story declarations."
            )

        # Collect transition rules
        if not is_story:
            for rule in ctx.transitionRule():
                self._visit_transition_rule(rule, story, phase_name)

        # Visit agent blocks
        for agent_block in ctx.agentBlock():
            self._visit_agent_block(agent_block, story)

    def _visit_transition_rule(self, ctx, story, from_phase):
        target      = ctx.phaseTarget()
        is_terminal = bool(target.END())
        to_phase    = None if is_terminal else target.ID().getText()
        event_name  = ctx.ID().getText()
        line        = ctx.start.line

        if not is_terminal and to_phase not in story.phases:
            self.reporter.error(
                line, target.start.column, len(to_phase),
                f"Phase '{to_phase}' is not declared in story '{story.name}'.",
                f"Add 'PHASE {to_phase}.' to the story declarations."
            )
            return

        if event_name not in story.events:
            self.reporter.error(
                line, ctx.ID().symbol.column, len(event_name),
                f"Event '{event_name}' is not declared.",
                f"Add 'EVENT {event_name} <ORIGIN>.' to the story declarations."
            )
            return

        event_origin = story.events[event_name].origin

        story.transitions.append(TransitionInfo(
            from_phase   = from_phase,
            to_phase     = to_phase,
            is_terminal  = is_terminal,
            event_name   = event_name,
            event_origin = event_origin,
            cond_ctx     = ctx.condExpr() if ctx.IF() else None,
            line         = line,
        ))

    # == Story-level declaration ===============================================

    def _visit_story_declaration(
        self,
        ctx:   RegiaScriptParser.DeclarationContext,
        story: StoryInfo
    ):
        doc = parse_doc_comments(ctx.DOC_COMMENT())
        if ctx.actionDecl():
            _register_action(ctx.actionDecl(), story.actions,
                             self.reporter, doc)
        elif ctx.eventDecl():
            _register_event(ctx.eventDecl(), story.events,
                           self.reporter, doc)
        elif ctx.conditionDecl():
            _register_condition(ctx.conditionDecl(), story.conditions,
                               self.reporter, doc)

    # == Agent block ===========================================================

    def _visit_agent_block(self, ctx, story):
        doc  = parse_doc_comments(ctx.DOC_COMMENT())
        name = ctx.ID().getText()
        line = ctx.start.line

        if not story.is_default and name not in story.agents:
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Agent '{name}' is not declared in story '{story.name}'.",
                f"Add 'AGENT {name}.' to the story declarations."
            )
            return

        if story.is_default and name not in story.agents:
            agent = AgentInfo(name=name, line=line, doc=doc)
            story.agents[name] = agent
            story.agent_names.append(name)

        agent = story.agents[name]

        for section in ctx.agentSection():
            self._visit_agent_section(section, agent, story)

    # == Agent section =========================================================

    def _visit_agent_section(self, ctx, agent, story):
        doc = parse_doc_comments(ctx.DOC_COMMENT())
        if ctx.actionDecl():
            _register_action(ctx.actionDecl(), agent.actions,
                            self.reporter, doc)
        elif ctx.eventDecl():
            _register_event(ctx.eventDecl(), agent.events,
                        self.reporter, doc)
        elif ctx.conditionDecl():
            _register_condition(ctx.conditionDecl(), agent.conditions,
                            self.reporter, doc)

