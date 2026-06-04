"""
RegiaScript v2 compiler test suite.
Run with: python -m pytest tests/test_regiascript.py -v
"""

import unittest
from pathlib import Path
from src.compiler import compile_file, CompileResult

RGS = Path("tests/rgs")
EXP = Path("tests/expected")


def compile(category: str, filename: str) -> CompileResult:
    return compile_file(RGS / category / filename)


def expected(filename: str) -> str:
    return (EXP / "integration" / filename).read_text(
        encoding="utf-8"
    ).strip()


def get_output(result: CompileResult, agent: str) -> str:
    """Extract a specific agent's output from a CompileResult."""
    return result.outputs.get(agent, "").strip()


# ── Category A - Valid syntax ─────────────────────────────────────────────────

class TestValidSyntax(unittest.TestCase):

    def _assert_valid(self, filename: str):
        result = compile("valid", filename)
        self.assertEqual(
            result.error_count, 0,
            f"{filename} should be valid but got "
            f"{result.error_count} error(s):\n"
            + "\n".join(m.message for m in result.messages)
        )

    def test_default_story_only(self):
        self._assert_valid("default_story_only.rgs")

    def test_named_story_no_phases(self):
        self._assert_valid("named_story_no_phases.rgs")

    def test_named_story_with_phases(self):
        self._assert_valid("named_story_with_phases.rgs")

    def test_multiple_phases(self):
        self._assert_valid("multiple_phases.rgs")

    def test_multiple_agents(self):
        self._assert_valid("multiple_agents.rgs")

    def test_during_always_in_named_story(self):
        self._assert_valid("during_always_in_named_story.rgs")

    def test_all_origins(self):
        self._assert_valid("all_origins.rgs")

    def test_condition_not(self):
        self._assert_valid("condition_not.rgs")

    def test_condition_and(self):
        self._assert_valid("condition_and.rgs")

    def test_condition_or(self):
        self._assert_valid("condition_or.rgs")

    def test_condition_parentheses(self):
        self._assert_valid("condition_parentheses.rgs")

    def test_do_believe_forget(self):
        self._assert_valid("do_believe_forget.rgs")

    def test_multiple_actions_in_do(self):
        self._assert_valid("multiple_actions_in_do.rgs")

    def test_agent_local_declarations(self):
        self._assert_valid("agent_local_declarations.rgs")

    def test_multiple_stories(self):
        self._assert_valid("multiple_stories.rgs")

    def test_doc_comments(self):
        self._assert_valid("doc_comments.rgs")

    def test_plain_comments(self):
        self._assert_valid("plain_comments.rgs")

    def test_flat_formatting(self):
        self._assert_valid("flat_formatting.rgs")

    def test_enter_in_always_block(self):
        self._assert_valid("enter_in_always_block.rgs")


# ── Category B - Syntax errors ────────────────────────────────────────────────

class TestSyntaxErrors(unittest.TestCase):

    def _assert_syntax_error(self, filename: str):
        result = compile("syntax_errors", filename)
        self.assertGreater(
            result.error_count, 0,
            f"{filename} should have a syntax error but compiled cleanly."
        )

    def test_missing_story_keyword(self):
        self._assert_syntax_error("missing_story_keyword.rgs")

    def test_named_story_missing_priority_keyword(self):
        self._assert_syntax_error("named_story_missing_priority_keyword.rgs")

    def test_named_story_missing_priority_number(self):
        self._assert_syntax_error("named_story_missing_priority_number.rgs")

    def test_named_story_missing_period(self):
        self._assert_syntax_error("named_story_missing_period.rgs")

    def test_default_story_missing_period(self):
        self._assert_syntax_error("default_story_missing_period.rgs")

    def test_agent_missing_name(self):
        self._assert_syntax_error("agent_missing_name.rgs")

    def test_agent_missing_colon(self):
        self._assert_syntax_error("agent_missing_colon.rgs")

    def test_phase_missing_name(self):
        self._assert_syntax_error("phase_missing_name.rgs")

    def test_phase_missing_period(self):
        self._assert_syntax_error("phase_missing_period.rgs")

    def test_action_missing_name(self):
        self._assert_syntax_error("action_missing_name.rgs")

    def test_action_missing_period(self):
        self._assert_syntax_error("action_missing_period.rgs")

    def test_event_missing_origin(self):
        self._assert_syntax_error("event_missing_origin.rgs")

    def test_during_missing_phase(self):
        self._assert_syntax_error("during_missing_phase.rgs")

    def test_during_missing_colon(self):
        self._assert_syntax_error("during_missing_colon.rgs")

    def test_during_no_when_blocks(self):
        self._assert_syntax_error("during_no_when_blocks.rgs")

    def test_when_missing_event(self):
        self._assert_syntax_error("when_missing_event.rgs")

    def test_when_missing_origin(self):
        self._assert_syntax_error("when_missing_origin.rgs")

    def test_when_missing_colon(self):
        self._assert_syntax_error("when_missing_colon.rgs")

    def test_when_if_no_condition(self):
        self._assert_syntax_error("when_if_no_condition.rgs")

    def test_do_missing_action(self):
        self._assert_syntax_error("do_missing_action.rgs")

    def test_do_believe_missing_name(self):
        self._assert_syntax_error("do_believe_missing_name.rgs")

    def test_enter_missing_phase(self):
        self._assert_syntax_error("enter_missing_phase.rgs")

    def test_unclosed_parenthesis(self):
        self._assert_syntax_error("unclosed_parenthesis.rgs")

    def test_and_no_right_operand(self):
        self._assert_syntax_error("and_no_right_operand.rgs")


# ── Category C - Declaration errors ──────────────────────────────────────────

class TestDeclarationErrors(unittest.TestCase):

    def _assert_errors(self, filename: str, expected_count: int):
        result = compile("declaration_errors", filename)
        self.assertFalse(result.success)
        self.assertEqual(
            result.error_count, expected_count,
            f"{filename}: expected {expected_count} error(s), "
            f"got {result.error_count}."
        )

    def test_duplicate_story(self):
        self._assert_errors("duplicate_story.rgs", 1)

    def test_duplicate_default_story(self):
        self._assert_errors("duplicate_default_story.rgs", 1)

    def test_priority_zero(self):
        self._assert_errors("priority_zero.rgs", 1)

    def test_duplicate_phase(self):
        self._assert_errors("duplicate_phase.rgs", 1)

    def test_duplicate_agent_in_story(self):
        self._assert_errors("duplicate_agent_in_story.rgs", 1)

    def test_duplicate_story_action(self):
        self._assert_errors("duplicate_story_action.rgs", 1)

    def test_duplicate_story_event(self):
        self._assert_errors("duplicate_story_event.rgs", 1)


# ── Category D - Semantic errors ──────────────────────────────────────────────

class TestSemanticErrors(unittest.TestCase):

    def _assert_errors(self, filename: str, expected_count: int):
        result = compile("semantic_errors", filename)
        self.assertFalse(result.success)
        self.assertEqual(
            result.error_count, expected_count,
            f"{filename}: expected {expected_count} error(s), "
            f"got {result.error_count}."
        )

    def test_undeclared_event(self):
        self._assert_errors("undeclared_event.rgs", 1)

    def test_wrong_origin_event(self):
        self._assert_errors("wrong_origin_event.rgs", 1)

    def test_undeclared_action(self):
        self._assert_errors("undeclared_action.rgs", 1)

    def test_undeclared_condition_if(self):
        self._assert_errors("undeclared_condition_if.rgs", 1)

    def test_wrong_origin_condition(self):
        self._assert_errors("wrong_origin_condition.rgs", 1)

    def test_undeclared_condition_believe(self):
        self._assert_errors("undeclared_condition_believe.rgs", 1)

    def test_undeclared_condition_forget(self):
        self._assert_errors("undeclared_condition_forget.rgs", 1)

    def test_undeclared_phase_in_during(self):
        self._assert_errors("undeclared_phase_in_during.rgs", 1)

    def test_undeclared_phase_in_enter(self):
        self._assert_errors("undeclared_phase_in_enter.rgs", 1)

    def test_enter_in_default_story(self):
        self._assert_errors("enter_in_default_story.rgs", 1)


# ── Category E - Warnings ─────────────────────────────────────────────────────

class TestWarnings(unittest.TestCase):

    def _assert_warnings(self, filename: str, expected_count: int):
        result = compile("warnings", filename)
        self.assertTrue(
            result.success,
            f"{filename} should compile but failed with "
            f"{result.error_count} error(s)."
        )
        self.assertEqual(
            result.warning_count, expected_count,
            f"{filename}: expected {expected_count} warning(s), "
            f"got {result.warning_count}."
        )

    def test_unused_action(self):
        self._assert_warnings("unused_action.rgs", 1)

    def test_unused_event(self):
        self._assert_warnings("unused_event.rgs", 1)

    def test_unused_condition(self):
        self._assert_warnings("unused_condition.rgs", 1)

    def test_multiple_unused(self):
        self._assert_warnings("multiple_unused.rgs", 3)


# ── Category F - Output correctness ──────────────────────────────────────────

class TestOutputCorrectness(unittest.TestCase):

    def _assert_output(self, filename: str, agent: str):
        result = compile("integration", filename)
        self.assertTrue(
            result.success,
            f"{filename} failed to compile: "
            + "\n".join(m.message for m in result.messages)
        )
        snapshot_name = filename.replace(".rgs", f"_{agent}.asl")
        actual   = get_output(result, agent)
        snapshot = expected(snapshot_name)

        # Strip transition plans - only compare regular plans
        actual_plans   = _extract_plans(actual)
        snapshot_plans = snapshot.strip()

        self.assertEqual(
            actual_plans, snapshot_plans,
            f"{filename} [{agent}]: output does not match snapshot.\n"
            f"--- Expected ---\n{snapshot_plans}\n"
            f"--- Got ---\n{actual_plans}"
        )

    def test_default_story_plan(self):
        self._assert_output("default_story_plan.rgs", "Guard")

    def test_named_story_unconditional(self):
        self._assert_output("named_story_unconditional.rgs", "Hero")

    def test_named_story_always_plan(self):
        self._assert_output("named_story_always_plan.rgs", "Hero")

    def test_condition_not(self):
        self._assert_output("condition_not.rgs", "Hero")

    def test_condition_and(self):
        self._assert_output("condition_and.rgs", "Hero")

    def test_condition_or(self):
        self._assert_output("condition_or.rgs", "Hero")

    def test_condition_parentheses(self):
        self._assert_output("condition_parentheses.rgs", "Hero")

    def test_do_believe(self):
        self._assert_output("do_believe.rgs", "Hero")

    def test_do_forget(self):
        self._assert_output("do_forget.rgs", "Hero")

    def test_multiple_actions(self):
        self._assert_output("multiple_actions.rgs", "Hero")

    def test_environment_origin(self):
        self._assert_output("environment_origin.rgs", "Hero")

    def test_director_origin(self):
        self._assert_output("director_origin.rgs", "Hero")

    def test_player_origin(self):
        self._assert_output("player_origin.rgs", "Hero")

    def test_timer_origin(self):
        self._assert_output("timer_origin.rgs", "Hero")

    def test_myself_origin(self):
        self._assert_output("myself_origin.rgs", "Hero")

    def test_priority_sorting(self):
        self._assert_output("priority_sorting.rgs", "Hero")

    def test_enter_phase(self):
        self._assert_output("enter_phase.rgs", "Hero")

    def test_agent_local_declarations(self):
        self._assert_output("agent_local_declarations.rgs", "Hero")

    def test_multi_agent_citizen(self):
        self._assert_output("multi_agent.rgs", "Citizen")

    def test_multi_agent_player(self):
        self._assert_output("multi_agent.rgs", "Player")


# ── Helper - extract just the plans section ───────────────────────────────────

def _extract_plans(output: str) -> str:
    """
    Extracts only the regular plans section from an agent output,
    stripping the initial beliefs and transition plans sections.
    This lets integration tests focus on plan correctness without
    being sensitive to transition plan details.
    """
    marker = "// ── Plans "
    idx    = output.find(marker)
    if idx == -1:
        return output.strip()
    # Skip the marker line itself
    after = output[idx:]
    lines  = after.splitlines()[1:]
    return "\n".join(lines).strip()


if __name__ == "__main__":
    unittest.main(verbosity=2)