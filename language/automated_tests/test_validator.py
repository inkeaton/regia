"""
Pass 4 tests: Semantic validator.

These tests verify that the Validator correctly catches semantic
errors (undeclared references, duplicates, structural violations)
and emits appropriate warnings (unused declarations).

Each test compiles a Regia source string through the full pipeline
and checks the resulting CompileResult for expected errors/warnings.

Run with:  pytest tests/test_validator.py -v
"""

import pytest

from regia.compiler import compile_source, CompileResult
from regia.errors import Severity


def _compile(source: str) -> CompileResult:
    """Compile source through the full pipeline.

    Args:
        source: Regia source code string.

    Returns:
        A CompileResult with diagnostics.
    """
    return compile_source(source)


def _error_messages(result: CompileResult) -> list[str]:
    """Extract error message strings from a CompileResult.

    Args:
        result: The compilation result.

    Returns:
        List of error message strings.
    """
    return [
        m.message for m in result.messages
        if m.severity == Severity.ERROR
    ]


def _warning_messages(result: CompileResult) -> list[str]:
    """Extract warning message strings from a CompileResult.

    Args:
        result: The compilation result.

    Returns:
        List of warning message strings.
    """
    return [
        m.message for m in result.messages
        if m.severity == Severity.WARNING
    ]


# == Duplicate Declarations ====================================================

class TestDuplicateDeclarations:
    """Tests for duplicate declaration errors."""

    def test_duplicate_action(self) -> None:
        """Two ACTIONs with the same name should error."""
        result = _compile("""
            ACTION greet.
            ACTION greet.
        """)
        errors = _error_messages(result)
        assert any("Duplicate action" in e and "greet" in e for e in errors)

    def test_duplicate_event(self) -> None:
        """Two EVENTs with the same name should error."""
        result = _compile("""
            EVENT alarm.
            EVENT alarm.
        """)
        errors = _error_messages(result)
        assert any("Duplicate event" in e and "alarm" in e for e in errors)

    def test_duplicate_fact(self) -> None:
        """Two FACTs with the same name should error."""
        result = _compile("""
            FACT happy.
            FACT happy.
        """)
        errors = _error_messages(result)
        assert any("Duplicate fact" in e and "happy" in e for e in errors)

    def test_duplicate_playbook(self) -> None:
        """Two PLAYBOOKs with the same name should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO a.
            PLAYBOOK P:
                WHEN e:
                    DO a.
        """)
        errors = _error_messages(result)
        assert any("Duplicate playbook" in e and "P" in e for e in errors)

    def test_different_namespaces_ok(self) -> None:
        """Same name in different namespaces should NOT error."""
        result = _compile("""
            ACTION greet.
            EVENT greet.
            FACT greet.
        """)
        errors = _error_messages(result)
        assert len(errors) == 0


# == Undeclared References =====================================================

class TestUndeclaredReferences:
    """Tests for undeclared reference errors."""

    def test_undeclared_action_in_playbook(self) -> None:
        """DO with an undeclared action should error."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO ghost_action.
        """)
        errors = _error_messages(result)
        assert any("Undeclared action" in e and "ghost_action" in e
                    for e in errors)

    def test_undeclared_event_in_when(self) -> None:
        """WHEN with an undeclared event should error."""
        result = _compile("""
            ACTION a.
            PLAYBOOK P:
                WHEN ghost_event:
                    DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared event" in e and "ghost_event" in e
                    for e in errors)

    def test_undeclared_fact_in_condition(self) -> None:
        """IF with an undeclared fact should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    IF ghost_fact:
                        DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared fact" in e and "ghost_fact" in e
                    for e in errors)

    def test_undeclared_fact_in_not_condition(self) -> None:
        """IF NOT with an undeclared fact should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    IF NOT ghost_fact:
                        DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared fact" in e and "ghost_fact" in e
                    for e in errors)

    def test_undeclared_playbook_in_assign(self) -> None:
        """ASSIGN with an undeclared playbook should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        ASSIGN GhostPlaybook TO R.
        """)
        errors = _error_messages(result)
        assert any("Undeclared playbook" in e and "GhostPlaybook" in e
                    for e in errors)

    def test_undeclared_role_in_assign(self) -> None:
        """ASSIGN TO an undeclared role should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO GhostRole.
        """)
        errors = _error_messages(result)
        assert any("Undeclared role" in e and "GhostRole" in e
                    for e in errors)

    def test_undeclared_role_in_role_do(self) -> None:
        """Role DO with an undeclared role should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    WHEN e:
                        Ghost DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared role" in e and "Ghost" in e
                    for e in errors)

    def test_special_actions_always_valid(self) -> None:
        """Special actions (TELL, BROADCAST, etc.) need no declaration."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO TELL(target, msg).
                    DO BROADCAST(alert).
                    DO ACHIEVE(goal).
                    DO BELIEVE(belief).
                    DO FORGET(old).
        """)
        errors = _error_messages(result)
        # No errors for the special actions themselves
        action_errors = [e for e in errors if "Undeclared action" in e]
        assert len(action_errors) == 0

    def test_undeclared_event_in_signal(self) -> None:
        """SIGNAL with an undeclared event should error."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO a.
                    SIGNAL ghost_signal.
        """)
        errors = _error_messages(result)
        assert any("Undeclared event" in e and "ghost_signal" in e
                    for e in errors)

    def test_undeclared_event_in_plot_when(self) -> None:
        """WHEN with an undeclared event should error."""
        result = _compile("""
            ACTION a.
            PLOT Q.
                PHASE start INITIAL.
                PHASE end.
                ROLE R.
                DURING start:
                    WHEN ghost_event:
                        TRANSITION TO end.
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared event" in e and "ghost_event" in e
                    for e in errors)

    def test_undeclared_phase_in_inline_transition(self) -> None:
        """Inline TRANSITION TO an undeclared phase should error."""
        result = _compile("""
            ACTION a.
            EVENT trigger.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    WHEN trigger:
                        TRANSITION TO ghost_phase.
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("undeclared phase" in e and "ghost_phase" in e
                    for e in errors)

    def test_undeclared_phase_in_during(self) -> None:
        """DURING an undeclared phase should error."""
        result = _compile("""
            ACTION a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING ghost_phase:
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("undeclared phase" in e and "ghost_phase" in e
                    for e in errors)

    def test_undeclared_fact_in_plot_if(self) -> None:
        """Plot IF with an undeclared fact should error."""
        result = _compile("""
            ACTION a.
            EVENT trigger.
            PLOT Q.
                PHASE start INITIAL.
                PHASE end.
                ROLE R.
                DURING start:
                    WHEN trigger:
                        IF ghost_fact:
                            TRANSITION TO end.
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("Undeclared fact" in e and "ghost_fact" in e
                    for e in errors)


# == Structural Constraints ====================================================

class TestStructuralConstraints:
    """Tests for structural rule violations."""

    def test_no_initial_phase(self) -> None:
        """A plot with no INITIAL phase should error."""
        result = _compile("""
            ACTION a.
            PLOT Q.
                PHASE start.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("no INITIAL phase" in e for e in errors)

    def test_multiple_initial_phases(self) -> None:
        """A plot with two INITIAL phases should error."""
        result = _compile("""
            ACTION a.
            PLOT Q.
                PHASE start INITIAL.
                PHASE middle INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("multiple INITIAL" in e for e in errors)

    def test_duplicate_on_enter(self) -> None:
        """Two ON ENTER blocks in the same DURING should error."""
        result = _compile("""
            ACTION a.
            ACTION b.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO a.
                    ON ENTER:
                        WORLD DO b.
        """)
        errors = _error_messages(result)
        assert any("Duplicate ON ENTER" in e for e in errors)

    def test_duplicate_on_exit(self) -> None:
        """Two ON EXIT blocks in the same DURING should error."""
        result = _compile("""
            ACTION a.
            ACTION b.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON EXIT:
                        WORLD DO a.
                    ON EXIT:
                        WORLD DO b.
        """)
        errors = _error_messages(result)
        assert any("Duplicate ON EXIT" in e for e in errors)

    def test_inline_transition_in_during_plot(self) -> None:
        """Inline TRANSITION inside DURING PLOT should error."""
        result = _compile("""
            ACTION a.
            EVENT trigger.
            PLOT Q.
                PHASE start INITIAL.
                PHASE end.
                ROLE R.
                DURING PLOT:
                    WHEN trigger:
                        TRANSITION TO end.
                    ON ENTER:
                        WORLD DO a.
        """)
        errors = _error_messages(result)
        assert any("TRANSITION TO cannot appear inside DURING PLOT" in e
                    for e in errors)


# == Unused Declarations =======================================================

class TestUnusedWarnings:
    """Tests for unused-declaration warnings."""

    def test_unused_action_warns(self) -> None:
        """A declared action that is never referenced should warn."""
        result = _compile("""
            ACTION used.
            ACTION unused_one.
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO used.
        """)
        warnings = _warning_messages(result)
        assert any("unused_one" in w and "never used" in w for w in warnings)

    def test_unused_event_warns(self) -> None:
        """A declared event that is never referenced should warn."""
        result = _compile("""
            ACTION a.
            EVENT used_event.
            EVENT unused_event.
            PLAYBOOK P:
                WHEN used_event:
                    DO a.
        """)
        warnings = _warning_messages(result)
        assert any("unused_event" in w and "never used" in w for w in warnings)

    def test_unused_fact_warns(self) -> None:
        """A declared fact that is never referenced should warn."""
        result = _compile("""
            ACTION a.
            EVENT e.
            FACT used_fact.
            FACT unused_fact.
            PLAYBOOK P:
                WHEN e:
                    IF used_fact:
                        DO a.
        """)
        warnings = _warning_messages(result)
        assert any("unused_fact" in w and "never used" in w for w in warnings)

    def test_unused_playbook_warns(self) -> None:
        """A declared playbook that is never ASSIGNed should warn."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK Used:
                WHEN e:
                    DO a.
            PLAYBOOK Unused:
                WHEN e:
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        ASSIGN Used TO R.
        """)
        warnings = _warning_messages(result)
        assert any("Unused" in w and "never used" in w for w in warnings)

    def test_all_used_no_warnings(self) -> None:
        """When everything is used, no unused warnings."""
        result = _compile("""
            ACTION greet.
            EVENT hello.
            FACT happy.
            PLAYBOOK Greeter:
                WHEN hello:
                    IF happy:
                        DO greet.
            PLOT P.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        ASSIGN Greeter TO R.
        """)
        warnings = _warning_messages(result)
        unused_warnings = [w for w in warnings if "never used" in w]
        assert len(unused_warnings) == 0


# == Valid Programs ============================================================

class TestValidPrograms:
    """Tests that well-formed programs pass validation cleanly."""

    def test_full_concert_example(self) -> None:
        """The full Concert example should have zero errors."""
        source = """
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
        result = _compile(source)
        assert result.success, (
            f"Expected success but got {result.error_count} error(s): "
            + "; ".join(_error_messages(result))
        )
        assert result.error_count == 0
