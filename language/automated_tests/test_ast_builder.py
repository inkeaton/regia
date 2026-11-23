"""
Pass 3 tests: AST builder.

These tests verify that the Lark Transformer correctly converts
parse trees into typed AST nodes with the right structure, values,
and source locations.

Each test parses a Regia source string, transforms it with the
ASTBuilder, and asserts on the resulting AST node types and fields.

Run with:  pytest tests/test_ast_builder.py -v
"""

import pytest

from regia.parser import parse
from regia.ast_builder import ASTBuilder
from regia.ast_nodes import (
    Program, ActionDecl, EventDecl, FactDecl,
    PlaybookDef, PbWhenBlock, DoStmt, SignalStmt,
    PbIfBranch, PbElseBranch,
    PlotDef, PhaseDecl, RoleDecl, DuringBlock,
    OnEnter, OnExit, PlotWhenBlock,
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    PlotIfBranch, PlotElseBranch,
    FactRef, ConditionNot, ConditionAnd, ConditionOr, Arg,
)


def _build(source: str) -> Program:
    """Parse and transform source code into an AST.

    Args:
        source: Regia source code string.

    Returns:
        The root Program AST node.
    """
    tree = parse(source)
    return ASTBuilder().transform(tree)


# == Base Element Declarations =================================================

class TestActionDecl:
    """Tests for ACTION declarations -> ActionDecl AST nodes."""

    def test_bare_action(self) -> None:
        """ACTION greet. -> ActionDecl with empty params."""
        ast = _build("ACTION greet.")
        assert len(ast.items) == 1
        action = ast.items[0]
        assert isinstance(action, ActionDecl)
        assert action.name == "greet"
        assert action.params == []

    def test_action_with_params(self) -> None:
        """ACTION give(item, target). -> ActionDecl with 2 params."""
        ast = _build("ACTION give(item, target).")
        action = ast.items[0]
        assert isinstance(action, ActionDecl)
        assert action.name == "give"
        assert action.params == ["item", "target"]

    def test_action_source_location(self) -> None:
        """ActionDecl should carry source location."""
        ast = _build("ACTION greet.")
        assert ast.items[0].loc.line > 0


class TestEventDecl:
    """Tests for EVENT declarations -> EventDecl AST nodes."""

    def test_bare_event(self) -> None:
        """EVENT fan_greets. -> EventDecl with no origin."""
        ast = _build("EVENT fan_greets.")
        event = ast.items[0]
        assert isinstance(event, EventDecl)
        assert event.name == "fan_greets"


class TestFactDecl:
    """Tests for FACT declarations -> FactDecl AST nodes."""

    def test_bare_fact(self) -> None:
        """FACT happy. -> FactDecl with empty params."""
        ast = _build("FACT happy.")
        fact = ast.items[0]
        assert isinstance(fact, FactDecl)
        assert fact.name == "happy"
        assert fact.params == []

    def test_fact_with_params(self) -> None:
        """FACT has_item(item). -> FactDecl with 1 param."""
        ast = _build("FACT has_item(item).")
        fact = ast.items[0]
        assert fact.name == "has_item"
        assert fact.params == ["item"]


# == Playbook ==================================================================

class TestPlaybookDef:
    """Tests for PLAYBOOK definitions -> PlaybookDef AST nodes."""

    def test_simple_playbook(self) -> None:
        """A playbook with one unconditional WHEN block."""
        ast = _build("""
            PLAYBOOK Guard:
                WHEN alarm:
                    DO run.
        """)
        pb = ast.items[0]
        assert isinstance(pb, PlaybookDef)
        assert pb.name == "Guard"
        assert len(pb.when_blocks) == 1

    def test_when_block_event(self) -> None:
        """WHEN block should capture the event name."""
        ast = _build("""
            PLAYBOOK P:
                WHEN fan_greets:
                    DO wave.
        """)
        when = ast.items[0].when_blocks[0]
        assert isinstance(when, PbWhenBlock)
        assert when.event == "fan_greets"

    def test_when_block_priority(self) -> None:
        """WHEN block with PRIORITY should capture the value."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event PRIORITY 7:
                    DO act.
        """)
        when = ast.items[0].when_blocks[0]
        assert when.priority == 7

    def test_when_block_no_priority(self) -> None:
        """WHEN block without PRIORITY should have None."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event:
                    DO act.
        """)
        when = ast.items[0].when_blocks[0]
        assert when.priority is None

    def test_unconditional_body(self) -> None:
        """Pure unconditional WHEN body -> prefix_stmts only."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event:
                    DO a.
                    DO b.
        """)
        when = ast.items[0].when_blocks[0]
        assert len(when.prefix_stmts) == 2
        assert len(when.branches) == 0
        assert when.else_branch is None

    def test_conditional_body(self) -> None:
        """Pure conditional WHEN body -> branches only."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event:
                    IF happy:
                        DO greet.
                    ELSE:
                        DO ignore.
        """)
        when = ast.items[0].when_blocks[0]
        assert len(when.prefix_stmts) == 0
        assert len(when.branches) == 1
        assert when.else_branch is not None

    def test_mixed_body(self) -> None:
        """Mixed WHEN body -> prefix + branches + else."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event:
                    DO log.
                    IF happy:
                        DO greet.
                    ELSE:
                        DO ignore.
        """)
        when = ast.items[0].when_blocks[0]
        assert len(when.prefix_stmts) == 1
        assert when.prefix_stmts[0].action == "log"
        assert len(when.branches) == 1
        assert when.else_branch is not None

    def test_multiple_if_branches(self) -> None:
        """Multiple IF branches should all be captured."""
        ast = _build("""
            PLAYBOOK P:
                WHEN event:
                    IF happy:
                        DO greet.
                    IF angry:
                        DO curse.
                    ELSE:
                        DO ignore.
        """)
        when = ast.items[0].when_blocks[0]
        assert len(when.branches) == 2
        assert isinstance(when.branches[0], PbIfBranch)
        assert isinstance(when.branches[1], PbIfBranch)


# == DoStmt and SignalStmt =====================================================

class TestDoStmt:
    """Tests for DO statements -> DoStmt AST nodes."""

    def test_simple_do(self) -> None:
        """DO greet. -> DoStmt with regular action."""
        ast = _build("""
            PLAYBOOK P:
                WHEN e:
                    DO greet.
        """)
        stmt = ast.items[0].when_blocks[0].prefix_stmts[0]
        assert isinstance(stmt, DoStmt)
        assert stmt.action == "greet"
        assert stmt.is_special is False
        assert stmt.args == []

    def test_do_with_args(self) -> None:
        """DO give(sword, 3). -> DoStmt with mixed args."""
        ast = _build("""
            PLAYBOOK P:
                WHEN e:
                    DO give(sword, 3).
        """)
        stmt = ast.items[0].when_blocks[0].prefix_stmts[0]
        assert stmt.action == "give"
        assert len(stmt.args) == 2
        assert isinstance(stmt.args[0], Arg)
        assert stmt.args[0].value == "sword"
        assert stmt.args[1].value == 3

    def test_do_tell_is_special(self) -> None:
        """DO TELL(player, msg). -> DoStmt with is_special=True."""
        ast = _build("""
            PLAYBOOK P:
                WHEN e:
                    DO TELL(player, msg).
        """)
        stmt = ast.items[0].when_blocks[0].prefix_stmts[0]
        assert stmt.action == "TELL"
        assert stmt.is_special is True
        assert len(stmt.args) == 2

    def test_all_special_actions(self) -> None:
        """All five special actions should set is_special=True."""
        source = """
            PLAYBOOK P:
                WHEN e:
                    DO TELL(a, b).
                WHEN f:
                    DO BROADCAST(x).
                WHEN g:
                    DO ACHIEVE(goal).
                WHEN h:
                    DO BELIEVE(fact).
                WHEN i:
                    DO FORGET(old).
        """
        ast = _build(source)
        pb = ast.items[0]
        for when in pb.when_blocks:
            stmt = when.prefix_stmts[0]
            assert stmt.is_special is True, f"{stmt.action} should be special"


class TestSignalStmt:
    """Tests for SIGNAL statements -> SignalStmt AST nodes."""

    def test_simple_signal(self) -> None:
        """SIGNAL emergency. -> SignalStmt."""
        ast = _build("""
            PLAYBOOK P:
                WHEN e:
                    SIGNAL emergency.
        """)
        stmt = ast.items[0].when_blocks[0].prefix_stmts[0]
        assert isinstance(stmt, SignalStmt)
        assert stmt.event == "emergency"
        assert stmt.args == []

    def test_signal_with_args(self) -> None:
        """SIGNAL alert(location, level). -> SignalStmt with args."""
        ast = _build("""
            PLAYBOOK P:
                WHEN e:
                    SIGNAL alert(location, level).
        """)
        stmt = ast.items[0].when_blocks[0].prefix_stmts[0]
        assert stmt.event == "alert"
        assert len(stmt.args) == 2


# == Conditions ================================================================

class TestConditions:
    """Tests for condition expressions -> Condition AST nodes."""

    def _condition_from(self, source: str) -> object:
        """Extract the condition from a minimal IF branch.

        Args:
            source: Full source with a PLAYBOOK containing an IF.

        Returns:
            The ConditionExpr from the first IF branch.
        """
        ast = _build(source)
        return ast.items[0].when_blocks[0].branches[0].condition

    def test_simple_fact_collapses(self) -> None:
        """IF happy: -> should collapse to bare FactRef (no wrappers)."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF happy:
                        DO a.
        """)
        assert isinstance(cond, FactRef)
        assert cond.name == "happy"

    def test_parameterised_fact(self) -> None:
        """IF has_item(sword): -> FactRef with args."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF has_item(sword):
                        DO a.
        """)
        assert isinstance(cond, FactRef)
        assert cond.name == "has_item"
        assert len(cond.args) == 1
        assert cond.args[0].value == "sword"

    def test_not_wraps(self) -> None:
        """IF NOT angry: -> ConditionNot(FactRef)."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF NOT angry:
                        DO a.
        """)
        assert isinstance(cond, ConditionNot)
        assert isinstance(cond.operand, FactRef)
        assert cond.operand.name == "angry"

    def test_and_creates_node(self) -> None:
        """IF happy AND healthy: -> ConditionAnd with 2 operands."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF happy AND healthy:
                        DO a.
        """)
        assert isinstance(cond, ConditionAnd)
        assert len(cond.operands) == 2
        assert all(isinstance(op, FactRef) for op in cond.operands)

    def test_or_creates_node(self) -> None:
        """IF happy OR neutral: -> ConditionOr with 2 operands."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF happy OR neutral:
                        DO a.
        """)
        assert isinstance(cond, ConditionOr)
        assert len(cond.operands) == 2

    def test_complex_precedence(self) -> None:
        """IF (happy OR neutral) AND NOT busy: -> correct nesting."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF (happy OR neutral) AND NOT busy:
                        DO a.
        """)
        # Top level: AND
        assert isinstance(cond, ConditionAnd)
        assert len(cond.operands) == 2
        # Left: (happy OR neutral) - parentheses unwrapped
        left = cond.operands[0]
        assert isinstance(left, ConditionOr)
        assert len(left.operands) == 2
        # Right: NOT busy
        right = cond.operands[1]
        assert isinstance(right, ConditionNot)
        assert isinstance(right.operand, FactRef)
        assert right.operand.name == "busy"

    def test_numeric_fact_arg(self) -> None:
        """IF at_level(3): -> FactRef with numeric arg."""
        cond = self._condition_from("""
            PLAYBOOK P:
                WHEN e:
                    IF at_level(3):
                        DO a.
        """)
        assert isinstance(cond, FactRef)
        assert cond.args[0].value == 3


# == Plot ======================================================================

class TestPlotDef:
    """Tests for PLOT definitions -> PlotDef AST nodes."""

    def test_plot_name(self) -> None:
        """PlotDef should capture the name."""
        ast = _build("""
            PLOT Concert.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        WORLD DO begin.
        """)
        plot = ast.items[0]
        assert isinstance(plot, PlotDef)
        assert plot.name == "Concert"

    def test_phases(self) -> None:
        """PlotDef should separate phases from roles."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    ON ENTER:
                        WORLD DO x.
        """)
        plot = ast.items[0]
        assert len(plot.phases) == 2
        assert len(plot.roles) == 1

    def test_initial_phase(self) -> None:
        """PHASE x INITIAL. -> PhaseDecl(is_initial=True)."""
        ast = _build("""
            PLOT Q.
                PHASE start INITIAL.
                PHASE end.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO x.
        """)
        plot = ast.items[0]
        assert plot.phases[0].is_initial is True
        assert plot.phases[0].name == "start"
        assert plot.phases[1].is_initial is False


class TestDuringBlock:
    """Tests for DURING blocks -> DuringBlock AST nodes."""

    def test_during_phase(self) -> None:
        """DURING backstage: -> DuringBlock with phase_name."""
        ast = _build("""
            PLOT Q.
                PHASE backstage INITIAL.
                ROLE R.
                DURING backstage:
                    ON ENTER:
                        WORLD DO start.
        """)
        block = ast.items[0].during_blocks[0]
        assert isinstance(block, DuringBlock)
        assert block.phase_name == "backstage"

    def test_during_plot_wide(self) -> None:
        """DURING PLOT: -> DuringBlock with phase_name=None."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE R.
                DURING PLOT:
                    WHEN emergency:
                        WORLD DO alert.
        """)
        block = ast.items[0].during_blocks[0]
        assert block.phase_name is None

    def test_during_content_sorted(self) -> None:
        """Content inside a DURING block should be sorted by type."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    WHEN trigger:
                        TRANSITION TO b.
                    ON ENTER:
                        WORLD DO start.
                    ON EXIT:
                        WORLD DO stop.
                    WHEN alert:
                        WORLD DO evacuate.
        """)
        block = ast.items[0].during_blocks[0]
        assert len(block.on_enters) == 1
        assert len(block.on_exits) == 1
        assert len(block.when_blocks) == 2



class TestImperativeStmts:
    """Tests for imperative statements inside Plots."""

    def test_assign(self) -> None:
        """ASSIGN Pb TO Role. -> AssignStmt."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE R.
                DURING a:
                    ON ENTER:
                        ASSIGN MyPlaybook TO R.
        """)
        stmt = ast.items[0].during_blocks[0].on_enters[0].stmts[0]
        assert isinstance(stmt, AssignStmt)
        assert stmt.playbook == "MyPlaybook"
        assert stmt.role == "R"

    def test_unassign(self) -> None:
        """UNASSIGN Pb FROM Role. -> UnassignStmt."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE R.
                DURING a:
                    ON EXIT:
                        UNASSIGN MyPlaybook FROM R.
        """)
        stmt = ast.items[0].during_blocks[0].on_exits[0].stmts[0]
        assert isinstance(stmt, UnassignStmt)
        assert stmt.playbook == "MyPlaybook"
        assert stmt.role == "R"

    def test_world_do(self) -> None:
        """WORLD DO trigger_alarm. -> WorldDoStmt."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE R.
                DURING a:
                    ON ENTER:
                        WORLD DO trigger_alarm.
        """)
        stmt = ast.items[0].during_blocks[0].on_enters[0].stmts[0]
        assert isinstance(stmt, WorldDoStmt)
        assert stmt.action == "trigger_alarm"
        assert stmt.is_special is False

    def test_world_do_special(self) -> None:
        """WORLD DO BROADCAST(msg). -> WorldDoStmt(is_special=True)."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE R.
                DURING a:
                    ON ENTER:
                        WORLD DO BROADCAST(alert).
        """)
        stmt = ast.items[0].during_blocks[0].on_enters[0].stmts[0]
        assert stmt.is_special is True
        assert stmt.action == "BROADCAST"
        assert len(stmt.args) == 1

    def test_role_do(self) -> None:
        """Hero DO acknowledge. -> RoleDoStmt."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE Hero.
                DURING a:
                    WHEN alert:
                        Hero DO acknowledge.
        """)
        when = ast.items[0].during_blocks[0].when_blocks[0]
        stmt = when.prefix_stmts[0]
        assert isinstance(stmt, RoleDoStmt)
        assert stmt.role == "Hero"
        assert stmt.action == "acknowledge"

    def test_role_do_with_special_and_args(self) -> None:
        """Singer DO TELL(player, info). -> RoleDoStmt(is_special=True)."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE Singer.
                DURING a:
                    WHEN ask:
                        Singer DO TELL(player, info).
        """)
        stmt = ast.items[0].during_blocks[0].when_blocks[0].prefix_stmts[0]
        assert isinstance(stmt, RoleDoStmt)
        assert stmt.role == "Singer"
        assert stmt.action == "TELL"
        assert stmt.is_special is True
        assert len(stmt.args) == 2


class TestPlotWhenBlock:
    """Tests for Plot WHEN blocks -> PlotWhenBlock AST nodes."""

    def test_plot_when_body_separation(self) -> None:
        """Plot WHEN body should separate prefix, branches, else."""
        ast = _build("""
            PLOT Q.
                PHASE a INITIAL.
                ROLE Hero.
                DURING a:
                    ON ENTER:
                        WORLD DO start.
                    WHEN choice:
                        WORLD DO log.
                        IF heroic:
                            Hero DO fight.
                        ELSE:
                            Hero DO flee.
        """)
        when = ast.items[0].during_blocks[0].when_blocks[0]
        assert isinstance(when, PlotWhenBlock)
        assert len(when.prefix_stmts) == 1
        assert isinstance(when.prefix_stmts[0], WorldDoStmt)
        assert len(when.branches) == 1
        assert isinstance(when.branches[0], PlotIfBranch)
        assert when.else_branch is not None
        assert isinstance(when.else_branch, PlotElseBranch)


# == Full Example ==============================================================

class TestFullExample:
    """Tests the complete worked example produces a correct AST."""

    FULL_EXAMPLE = """
        ACTION greet_back.
        ACTION curse.
        ACTION ignore.
        ACTION flee.
        ACTION acknowledge.
        ACTION bow.
        ACTION perform_song.
        ACTION trigger_alarm.
        ACTION add_waiting_for_concert.
        ACTION announce_concert.
        ACTION start_music.

        EVENT fan_greets.
        EVENT player_asks_about_quest.
        EVENT time_to_start.
        EVENT emergency.
        EVENT song_ends.
        EVENT audience_cheers.

        FACT happy.
        FACT angry.
        FACT audience_satisfied.

        PLAYBOOK SingerInBackstage:
            WHEN fan_greets:
                IF happy:
                    DO greet_back.
                IF angry:
                    DO curse.
                ELSE:
                    DO ignore.

            WHEN player_asks_about_quest PRIORITY 7:
                DO TELL(player, busy_message).

            WHEN emergency:
                DO flee.
                SIGNAL emergency.

        PLAYBOOK SingerOnStage:
            WHEN audience_cheers:
                DO bow.
                DO ACHIEVE(perform_song).

        PLOT Concert.
            PHASE backstage INITIAL.
            PHASE performing.
            PHASE aftermath.
            ROLE Singer.
            ROLE AudienceMember.

            DURING PLOT:
                WHEN emergency PRIORITY 9:
                    WORLD DO trigger_alarm.
                    Singer DO acknowledge.
                    AudienceMember DO acknowledge.

            DURING backstage:
                WHEN time_to_start:
                    TRANSITION TO performing.
                ON ENTER:
                    ASSIGN SingerInBackstage TO Singer.
                    WORLD DO add_waiting_for_concert.
                ON EXIT:
                    UNASSIGN SingerInBackstage FROM Singer.
                    WORLD DO announce_concert.

            DURING performing:
                WHEN song_ends:
                    IF audience_satisfied:
                        TRANSITION TO aftermath.
                ON ENTER:
                    ASSIGN SingerOnStage TO Singer.
                    WORLD DO start_music.
                ON EXIT:
                    UNASSIGN SingerOnStage FROM Singer.
    """

    def test_ast_root(self) -> None:
        """The full example should produce a valid Program."""
        ast = _build(self.FULL_EXAMPLE)
        assert isinstance(ast, Program)
        # 11 actions + 6 events + 3 facts + 2 playbooks + 1 plot = 23
        assert len(ast.items) == 23

    def test_playbook_structure(self) -> None:
        """SingerInBackstage should have 3 WHEN blocks."""
        ast = _build(self.FULL_EXAMPLE)
        pbs = [i for i in ast.items if isinstance(i, PlaybookDef)]
        assert len(pbs) == 2
        sib = pbs[0]
        assert sib.name == "SingerInBackstage"
        assert len(sib.when_blocks) == 3

    def test_first_when_block_branches(self) -> None:
        """First WHEN block should have 2 IF + 1 ELSE."""
        ast = _build(self.FULL_EXAMPLE)
        sib = [i for i in ast.items if isinstance(i, PlaybookDef)][0]
        fan_greets = sib.when_blocks[0]
        assert fan_greets.event == "fan_greets"
        assert len(fan_greets.branches) == 2
        assert fan_greets.else_branch is not None

    def test_second_when_block_priority_and_tell(self) -> None:
        """Second WHEN block should have priority 7 and TELL."""
        ast = _build(self.FULL_EXAMPLE)
        sib = [i for i in ast.items if isinstance(i, PlaybookDef)][0]
        quest = sib.when_blocks[1]
        assert quest.event == "player_asks_about_quest"
        assert quest.priority == 7
        assert len(quest.prefix_stmts) == 1
        assert quest.prefix_stmts[0].action == "TELL"
        assert quest.prefix_stmts[0].is_special is True

    def test_third_when_block_mixed(self) -> None:
        """Third WHEN block should have DO + SIGNAL (mixed)."""
        ast = _build(self.FULL_EXAMPLE)
        sib = [i for i in ast.items if isinstance(i, PlaybookDef)][0]
        emg = sib.when_blocks[2]
        assert emg.event == "emergency"
        assert len(emg.prefix_stmts) == 2
        assert isinstance(emg.prefix_stmts[0], DoStmt)
        assert isinstance(emg.prefix_stmts[1], SignalStmt)

    def test_plot_structure(self) -> None:
        """Concert plot should have correct phases, roles, during blocks."""
        ast = _build(self.FULL_EXAMPLE)
        plot = [i for i in ast.items if isinstance(i, PlotDef)][0]
        assert plot.name == "Concert"
        assert len(plot.phases) == 3
        assert len(plot.roles) == 2
        assert len(plot.during_blocks) == 3

    def test_plot_initial_phase(self) -> None:
        """The backstage phase should be marked as initial."""
        ast = _build(self.FULL_EXAMPLE)
        plot = [i for i in ast.items if isinstance(i, PlotDef)][0]
        backstage = plot.phases[0]
        assert backstage.name == "backstage"
        assert backstage.is_initial is True

    def test_during_plot_wide_block(self) -> None:
        """DURING PLOT block should have phase_name=None."""
        ast = _build(self.FULL_EXAMPLE)
        plot = [i for i in ast.items if isinstance(i, PlotDef)][0]
        plot_wide = plot.during_blocks[0]
        assert plot_wide.phase_name is None
        assert len(plot_wide.when_blocks) == 1
        assert plot_wide.when_blocks[0].priority == 9

    def test_backstage_during_block(self) -> None:
        """Backstage DURING block should have correct structure."""
        ast = _build(self.FULL_EXAMPLE)
        plot = [i for i in ast.items if isinstance(i, PlotDef)][0]
        backstage_block = plot.during_blocks[1]
        assert backstage_block.phase_name == "backstage"
        assert len(backstage_block.when_blocks) == 1
        assert len(backstage_block.on_enters) == 1
        assert len(backstage_block.on_exits) == 1

    def test_guarded_transition_in_performing(self) -> None:
        """Performing phase transition should have a guard."""
        ast = _build(self.FULL_EXAMPLE)
        plot = [i for i in ast.items if isinstance(i, PlotDef)][0]
        perf_block = plot.during_blocks[2]
        when_block = perf_block.when_blocks[0]
        assert when_block.event == "song_ends"
        
        if_branch = when_block.branches[0]
        assert isinstance(if_branch.condition, FactRef)
        assert if_branch.condition.name == "audience_satisfied"
        tr = if_branch.stmts[0]
        assert tr.target_phase == "aftermath"
