"""
RegiaScript compiler test suite.
Run with:  python -m pytest tests/test_regiascript.py -v
       or: python -m unittest tests/test_regiascript -v
"""

import unittest
from pathlib import Path

from src.compiler import compile_file, CompileResult

# ── Paths ─────────────────────────────────────────────────────────────────────

RGS = Path("tests/rgs")
EXP = Path("tests/expected")


# ── Helpers ───────────────────────────────────────────────────────────────────

def compile(category: str, filename: str) -> CompileResult:
    return compile_file(RGS / category / filename)

def expected(filename: str) -> str:
    return (EXP / "integration" / filename).read_text(encoding="utf-8").strip()


# ── Category A — Valid syntax ─────────────────────────────────────────────────

class TestValidSyntax(unittest.TestCase):
    """Every file in rgs/valid/ must produce zero errors."""

    def _assert_valid(self, filename: str):
        result = compile("valid", filename)
        self.assertEqual(
            result.error_count, 0,
            f"{filename} should be valid but got {result.error_count} error(s):\n"
            + "\n".join(m.message for m in result.messages)
        )

    def test_empty_file(self):
        self._assert_valid("empty.rgs")

    def test_declarations_only(self):
        self._assert_valid("declarations_only.rgs")

    def test_always_unconditional(self):
        self._assert_valid("always_unconditional.rgs")

    def test_always_conditional(self):
        self._assert_valid("always_conditional.rgs")

    def test_named_story_unconditional(self):
        self._assert_valid("named_story_unconditional.rgs")

    def test_named_story_conditional(self):
        self._assert_valid("named_story_conditional.rgs")

    def test_condition_not(self):
        self._assert_valid("condition_not.rgs")

    def test_condition_and(self):
        self._assert_valid("condition_and.rgs")

    def test_condition_or(self):
        self._assert_valid("condition_or.rgs")

    def test_condition_parentheses(self):
        self._assert_valid("condition_parentheses.rgs")

    def test_condition_complex(self):
        self._assert_valid("condition_complex.rgs")

    def test_do_believe_forget(self):
        self._assert_valid("do_believe_forget.rgs")

    def test_multiple_actions(self):
        self._assert_valid("multiple_actions.rgs")

    def test_multiple_when_blocks(self):
        self._assert_valid("multiple_when_blocks.rgs")

    def test_multiple_during_blocks(self):
        self._assert_valid("multiple_during_blocks.rgs")

    def test_all_origins(self):
        self._assert_valid("all_origins.rgs")

    def test_doc_comments(self):
        self._assert_valid("doc_comments.rgs")

    def test_plain_comments(self):
        self._assert_valid("plain_comments.rgs")

    def test_flat_formatting(self):
        self._assert_valid("flat_formatting.rgs")


# ── Category B — Syntax errors ────────────────────────────────────────────────

class TestSyntaxErrors(unittest.TestCase):
    """Every file in rgs/syntax_errors/ must produce at least one error."""

    def _assert_syntax_error(self, filename: str):
        result = compile("syntax_errors", filename)
        self.assertGreater(
            result.error_count, 0,
            f"{filename} should have a syntax error but compiled cleanly."
        )

    def test_story_missing_name(self):
        self._assert_syntax_error("story_missing_name.rgs")

    def test_story_missing_priority_keyword(self):
        self._assert_syntax_error("story_missing_priority_keyword.rgs")

    def test_story_missing_priority_number(self):
        self._assert_syntax_error("story_missing_priority_number.rgs")

    def test_story_missing_period(self):
        self._assert_syntax_error("story_missing_period.rgs")

    def test_action_missing_name(self):
        self._assert_syntax_error("action_missing_name.rgs")

    def test_action_missing_period(self):
        self._assert_syntax_error("action_missing_period.rgs")

    def test_event_missing_name(self):
        self._assert_syntax_error("event_missing_name.rgs")

    def test_event_missing_origin(self):
        self._assert_syntax_error("event_missing_origin.rgs")

    def test_condition_missing_name(self):
        self._assert_syntax_error("condition_missing_name.rgs")

    def test_condition_missing_origin(self):
        self._assert_syntax_error("condition_missing_origin.rgs")

    def test_during_missing_story(self):
        self._assert_syntax_error("during_missing_story.rgs")

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

    def test_do_believe_missing_condition(self):
        self._assert_syntax_error("do_believe_missing_condition.rgs")

    def test_do_forget_missing_condition(self):
        self._assert_syntax_error("do_forget_missing_condition.rgs")

    def test_unclosed_parenthesis(self):
        self._assert_syntax_error("unclosed_parenthesis.rgs")

    def test_and_no_right_operand(self):
        self._assert_syntax_error("and_no_right_operand.rgs")

    def test_or_no_right_operand(self):
        self._assert_syntax_error("or_no_right_operand.rgs")


# ── Category C — Declaration errors ──────────────────────────────────────────

class TestDeclarationErrors(unittest.TestCase):
    """Files must fail in pass 1 with exactly the expected error count."""

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

    def test_duplicate_action(self):
        self._assert_errors("duplicate_action.rgs", 1)

    def test_duplicate_event(self):
        self._assert_errors("duplicate_event.rgs", 1)

    def test_duplicate_condition(self):
        self._assert_errors("duplicate_condition.rgs", 1)

    def test_priority_zero(self):
        self._assert_errors("priority_zero.rgs", 1)

    def test_multiple_duplicates(self):
        self._assert_errors("multiple_duplicates.rgs", 3)


# ── Category D — Semantic errors ──────────────────────────────────────────────

class TestSemanticErrors(unittest.TestCase):
    """Files must fail in pass 2 with exactly the expected error count."""

    def _assert_errors(self, filename: str, expected_count: int):
        result = compile("semantic_errors", filename)
        self.assertFalse(result.success)
        self.assertEqual(
            result.error_count, expected_count,
            f"{filename}: expected {expected_count} error(s), "
            f"got {result.error_count}."
        )

    def test_undeclared_story(self):
        self._assert_errors("undeclared_story.rgs", 1)

    def test_undeclared_event(self):
        self._assert_errors("undeclared_event.rgs", 1)

    def test_wrong_origin_event(self):
        self._assert_errors("wrong_origin_event.rgs", 1)

    def test_undeclared_condition_if(self):
        self._assert_errors("undeclared_condition_if.rgs", 1)

    def test_wrong_origin_condition(self):
        self._assert_errors("wrong_origin_condition.rgs", 1)

    def test_undeclared_action(self):
        self._assert_errors("undeclared_action.rgs", 1)

    def test_undeclared_condition_believe(self):
        self._assert_errors("undeclared_condition_believe.rgs", 1)

    def test_undeclared_condition_forget(self):
        self._assert_errors("undeclared_condition_forget.rgs", 1)


# ── Category E — Warnings ─────────────────────────────────────────────────────

class TestWarnings(unittest.TestCase):
    """Files must compile successfully but produce the expected warning count."""

    def _assert_warnings(self, filename: str, expected_count: int):
        result = compile("warnings", filename)
        self.assertTrue(
            result.success,
            f"{filename} should compile successfully but failed with "
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


# ── Category F — Output correctness ──────────────────────────────────────────

class TestOutputCorrectness(unittest.TestCase):
    """Compiled output must exactly match the stored snapshot."""

    def _assert_output(self, filename: str):
        result = compile("integration", filename)
        self.assertTrue(
            result.success,
            f"{filename} failed to compile: "
            + "\n".join(m.message for m in result.messages)
        )
        actual   = result.output.strip()
        snapshot = expected(filename.replace(".rgs", ".asl"))
        self.assertEqual(
            actual, snapshot,
            f"{filename}: output does not match snapshot.\n"
            f"--- Expected ---\n{snapshot}\n"
            f"--- Got ---\n{actual}"
        )

    def test_always_unconditional(self):
        self._assert_output("always_unconditional.rgs")

    def test_always_conditional(self):
        self._assert_output("always_conditional.rgs")

    def test_named_story_unconditional(self):
        self._assert_output("named_story_unconditional.rgs")

    def test_named_story_conditional(self):
        self._assert_output("named_story_conditional.rgs")

    def test_condition_not(self):
        self._assert_output("condition_not.rgs")

    def test_condition_and(self):
        self._assert_output("condition_and.rgs")

    def test_condition_or(self):
        self._assert_output("condition_or.rgs")

    def test_condition_or_with_story(self):
        self._assert_output("condition_or_with_story.rgs")

    def test_condition_parentheses(self):
        self._assert_output("condition_parentheses.rgs")

    def test_do_believe(self):
        self._assert_output("do_believe.rgs")

    def test_do_forget(self):
        self._assert_output("do_forget.rgs")

    def test_multiple_actions(self):
        self._assert_output("multiple_actions.rgs")

    def test_priority_sorting(self):
        self._assert_output("priority_sorting.rgs")

    def test_environment_origin(self):
        self._assert_output("environment_origin.rgs")

    def test_director_origin(self):
        self._assert_output("director_origin.rgs")

    def test_myself_origin(self):
        self._assert_output("myself_origin.rgs")


if __name__ == "__main__":
    unittest.main(verbosity=2)