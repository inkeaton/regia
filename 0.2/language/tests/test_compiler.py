"""
Smoke tests: verify the compiler pipeline works end-to-end.

Uses syrupy for snapshot testing of generated AgentSpeak output.
Run with:  pytest              (from the language/ directory)
Update:    pytest --snapshot-update   (to regenerate snapshots)
"""

from regia.compiler import compile_source


class TestSmoke:
    """Basic pipeline smoke tests using the v0.2 grammar."""

    def test_minimal_program_compiles(self) -> None:
        """A minimal valid program should compile without errors."""
        source = "ACTION greet."
        result = compile_source(source)
        assert result.success
        assert result.error_count == 0

    def test_playbook_compiles(self) -> None:
        """A simple playbook with all elements declared."""
        source = """
        ACTION run_to_post.
        EVENT alarm.

        PLAYBOOK Guard:
            WHEN alarm:
                DO run_to_post.
        """
        result = compile_source(source)
        assert result.success
        assert result.error_count == 0

    def test_plot_compiles(self) -> None:
        """A simple plot with all elements declared."""
        source = """
        ACTION begin_quest.

        PLOT Quest.
            PHASE start INITIAL.
            ROLE Hero.
            DURING start:
                ON ENTER:
                    WORLD DO begin_quest.
        """
        result = compile_source(source)
        assert result.success
        assert result.error_count == 0

    def test_syntax_error_reports_cleanly(self) -> None:
        """Invalid syntax should produce an error, not crash."""
        source = "ACTION ."  # missing name
        result = compile_source(source)
        assert not result.success
        assert result.error_count > 0
        assert len(result.messages) > 0

    def test_semantic_error_reports_cleanly(self) -> None:
        """Undeclared references should produce errors."""
        source = """
        PLAYBOOK P:
            WHEN ghost_event:
                DO ghost_action.
        """
        result = compile_source(source)
        assert not result.success
        assert result.error_count >= 2  # undeclared event + action


class TestSnapshots:
    """
    Snapshot tests: compare generated AgentSpeak output against
    stored snapshots. If output changes intentionally, run:

        pytest --snapshot-update

    to regenerate the snapshot files in __snapshots__/.
    """

    # TODO: Add snapshot tests once the emitter is implemented.
    pass
