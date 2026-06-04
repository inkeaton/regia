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
    actions:    dict[str, ActionInfo]    = field(default_factory=dict)
    events:     dict[str, EventInfo]     = field(default_factory=dict)
    conditions: dict[str, ConditionInfo] = field(default_factory=dict)
    doc:        dict                     = field(default_factory=dict)

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

    def visitDefaultStory(
        self, ctx: RegiaScriptParser.DefaultStoryContext
    ):
        doc  = parse_doc_comments(ctx.DOC_COMMENT())
        name = "DEFAULT"
        line = ctx.start.line

        if name in self.table.stories:
            self.reporter.error(
                line, 0, len(name),
                "Only one DEFAULT story is allowed per file.",
                "Merge all default agent behaviour into one "
                "STORY DEFAULT block."
            )
            return

        story = StoryInfo(
            name=name, priority=None,
            line=line, is_default=True, doc=doc
        )
        self.table.stories[name] = story

        for agent_block in ctx.agentBlock():
            self._visit_agent_block(agent_block, story)

    def visitNamedStory(
        self, ctx: RegiaScriptParser.NamedStoryContext
    ):
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
                f"First declared at line {prev}. "
                f"Remove one of the declarations."
            )
            return

        story = StoryInfo(
            name=name, priority=priority,
            line=line, is_default=False, doc=doc
        )
        self.table.stories[name] = story

        # Story-level declarations
        for decl in ctx.declaration():
            self._visit_story_declaration(decl, story)

        # Phase declarations
        phase_index = 0
        for phase_ctx in ctx.phaseDecl():

            phase_doc = parse_doc_comments(phase_ctx.DOC_COMMENT())
            phase_name = phase_ctx.ID().getText()
            phase_line = phase_ctx.start.line

            if phase_name in story.phases:
                self.reporter.error(
                    phase_line,
                    phase_ctx.ID().symbol.column,
                    len(phase_name),
                    f"Phase '{phase_name}' is declared more than once "
                    f"in story '{name}'.",
                    "Remove one of the PHASE declarations."
                )
            else:
                story.phases[phase_name] = PhaseInfo(
                    name=phase_name,
                    line=phase_line,
                    initial=(phase_index == 0),
                    doc=phase_doc
                )
                phase_index += 1

        # Agent blocks
        for agent_block in ctx.agentBlock():
            self._visit_agent_block(agent_block, story)

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

    def _visit_agent_block(
        self,
        ctx:   RegiaScriptParser.AgentBlockContext,
        story: StoryInfo
    ):
        doc  = parse_doc_comments(ctx.DOC_COMMENT())
        name = ctx.ID().getText()
        line = ctx.start.line

        if name in story.agents:
            self.reporter.error(
                line, ctx.ID().symbol.column, len(name),
                f"Agent '{name}' appears more than once in "
                f"story '{story.name}'.",
                f"Remove one of the AGENT {name} blocks."
            )
            return

        agent = AgentInfo(name=name, line=line, doc=doc)
        story.agents[name] = agent

        for section in ctx.agentSection():
            self._visit_agent_section(section, agent, story)

    # == Agent section =========================================================

    def _visit_agent_section(
        self,
        ctx:   RegiaScriptParser.AgentSectionContext,
        agent: AgentInfo,
        story: StoryInfo
    ):
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
        elif ctx.duringBlock():
            # Validate phase reference
            block     = ctx.duringBlock()
            phase_ref = block.phaseRef()

            if not phase_ref.ALWAYS():
                phase_name = phase_ref.ID().getText()
                
                if phase_name not in story.phases:
                    self.reporter.error(
                        block.start.line,
                        phase_ref.start.column,
                        len(phase_name),
                        f"Phase '{phase_name}' is not declared "
                        f"in story '{story.name}'.",
                        f"Add 'PHASE {phase_name}.' to the story "
                        f"declarations, or check the spelling."
                    )
            # Validate ENTER inside DEFAULT story
            if story.is_default:
                self._check_no_enter(block, story.name)

    def _check_no_enter(
        self,
        ctx:        RegiaScriptParser.DuringBlockContext,
        story_name: str
    ):
        for when in ctx.whenBlock():
            for action in when.doSequence().doAction():
                if action.ENTER():
                    self.reporter.error(
                        action.start.line,
                        action.start.column,
                        len("ENTER"),
                        f"ENTER is not valid inside STORY DEFAULT.",
                        "Phase transitions only apply to named stories "
                        "with PHASE declarations."
                    )