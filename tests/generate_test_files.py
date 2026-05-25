"""
Generates all RegiaScript test fixture files.
Run once from the project root: python tests/generate_test_files.py
"""

from pathlib import Path

# ── Helpers ───────────────────────────────────────────────────────────────────

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  wrote {path}")

RGS = Path("tests/rgs")
EXP = Path("tests/expected/integration")

# =============================================================================
# CATEGORY A — Valid syntax
# =============================================================================

def generate_valid():
    base = RGS / "valid"

    write(base / "empty.rgs", "")

    write(base / "declarations_only.rgs", """
STORY  a PRIORITY 1.
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
""")

    write(base / "always_unconditional.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")

    write(base / "always_conditional.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
        DO run.
""")

    write(base / "named_story_unconditional.rgs", """
STORY  a PRIORITY 1.
ACTION run.
EVENT  spotted ENVIRONMENT.

DURING a:
    WHEN spotted ENVIRONMENT:
        DO run.
""")

    write(base / "named_story_conditional.rgs", """
STORY  a PRIORITY 1.
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.

DURING a:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF:
        DO run.
""")

    write(base / "condition_not.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
        DO run.
""")

    write(base / "condition_and.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_armed MYSELF AND NOT is_tired MYSELF:
        DO run.
""")

    write(base / "condition_or.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_armed MYSELF OR is_tired MYSELF:
        DO run.
""")

    write(base / "condition_parentheses.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION is_tired  MYSELF.
CONDITION is_armed  MYSELF.
CONDITION door_open ENVIRONMENT.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF (is_tired MYSELF OR door_open ENVIRONMENT) AND NOT is_armed MYSELF:
        DO run.
""")

    write(base / "condition_complex.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
CONDITION a MYSELF.
CONDITION b MYSELF.
CONDITION c MYSELF.
CONDITION d MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF (a MYSELF OR b MYSELF) AND NOT (c MYSELF OR d MYSELF):
        DO run.
""")

    write(base / "do_believe_forget.rgs", """
ACTION run.
EVENT  spotted ENVIRONMENT.
EVENT  lost    ENVIRONMENT.
CONDITION is_armed MYSELF.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO BELIEVE is_armed.
    WHEN lost ENVIRONMENT:
        DO FORGET is_armed.
""")

    write(base / "multiple_actions.rgs", """
ACTION run.
ACTION hide.
ACTION dance.
EVENT  spotted ENVIRONMENT.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run,
        DO hide,
        DO dance.
""")

    write(base / "multiple_when_blocks.rgs", """
ACTION run.
ACTION hide.
EVENT  spotted ENVIRONMENT.
EVENT  lost    ENVIRONMENT.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
    WHEN lost ENVIRONMENT:
        DO hide.
""")

    write(base / "multiple_during_blocks.rgs", """
STORY  a PRIORITY 1.
STORY  b PRIORITY 2.
ACTION run.
EVENT  spotted ENVIRONMENT.

DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
DURING a:
    WHEN spotted ENVIRONMENT:
        DO run.
DURING b:
    WHEN spotted ENVIRONMENT:
        DO run.
""")

    write(base / "all_origins.rgs", """
ACTION run.
EVENT  env_event  ENVIRONMENT.
EVENT  dir_event  DIRECTOR.
EVENT  self_event MYSELF.
CONDITION env_cond  ENVIRONMENT.
CONDITION dir_cond  DIRECTOR.
CONDITION self_cond MYSELF.

DURING ALWAYS:
    WHEN env_event  ENVIRONMENT IF env_cond  ENVIRONMENT:
        DO run.
    WHEN dir_event  DIRECTOR    IF dir_cond  DIRECTOR:
        DO run.
    WHEN self_event MYSELF      IF self_cond MYSELF:
        DO run.
""")

    write(base / "doc_comments.rgs", """
# @NAME: Main story
# @MEANING: The primary narrative context
STORY  a PRIORITY 1.

# @NAME: Run action
# @MEANING: Makes the agent run
ACTION run.

# @NAME: Spotted event
# @MEANING: Enemy entered view
EVENT  spotted ENVIRONMENT.

# @NAME: Tiredness
# @MEANING: Whether the agent is tired
CONDITION is_tired MYSELF.

# @NAME: Alert behaviour
# @MEANING: What to do during alert
DURING a:
    # @NAME: React to sighting
    # @MEANING: Run when spotted unless tired
    WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
        DO run.
""")

    write(base / "plain_comments.rgs", """
# This is a plain comment
STORY  a PRIORITY 1.
# Another comment
ACTION run.
EVENT  spotted ENVIRONMENT. # inline comment
CONDITION is_tired MYSELF.

# Comment before during
DURING a:
    # Comment before when
    WHEN spotted ENVIRONMENT:
        DO run. # comment after action
""")

    write(base / "flat_formatting.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING a: WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF: DO run.
""")


# =============================================================================
# CATEGORY B — Syntax errors
# =============================================================================

def generate_syntax_errors():
    base = RGS / "syntax_errors"

    write(base / "story_missing_name.rgs", """
STORY PRIORITY 1.
""")
    write(base / "story_missing_priority_keyword.rgs", """
STORY a 1.
""")
    write(base / "story_missing_priority_number.rgs", """
STORY a PRIORITY.
""")
    write(base / "story_missing_period.rgs", """
STORY a PRIORITY 1
ACTION run.
""")
    write(base / "action_missing_name.rgs", """
ACTION.
""")
    write(base / "action_missing_period.rgs", """
ACTION run
EVENT spotted ENVIRONMENT.
""")
    write(base / "event_missing_name.rgs", """
EVENT ENVIRONMENT.
""")
    write(base / "event_missing_origin.rgs", """
EVENT spotted.
""")
    write(base / "condition_missing_name.rgs", """
CONDITION MYSELF.
""")
    write(base / "condition_missing_origin.rgs", """
CONDITION is_tired.
""")
    write(base / "during_missing_story.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "during_missing_colon.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "during_no_when_blocks.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "when_missing_event.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN ENVIRONMENT:
        DO run.
""")
    write(base / "when_missing_origin.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted:
        DO run.
""")
    write(base / "when_missing_colon.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT
        DO run.
""")
    write(base / "when_if_no_condition.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF:
        DO run.
""")
    write(base / "do_missing_action.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO.
""")
    write(base / "do_believe_missing_condition.rgs", """
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO BELIEVE.
""")
    write(base / "do_forget_missing_condition.rgs", """
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO FORGET.
""")
    write(base / "unclosed_parenthesis.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF (is_tired MYSELF OR is_armed MYSELF:
        DO run.
""")
    write(base / "and_no_right_operand.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF AND:
        DO run.
""")
    write(base / "or_no_right_operand.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF OR:
        DO run.
""")


# =============================================================================
# CATEGORY C — Declaration errors
# =============================================================================

def generate_declaration_errors():
    base = RGS / "declaration_errors"

    write(base / "duplicate_story.rgs", """
STORY a PRIORITY 1.
STORY a PRIORITY 2.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "duplicate_action.rgs", """
STORY a PRIORITY 1.
ACTION run.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "duplicate_event.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "duplicate_condition.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF:
        DO run.
""")
    write(base / "priority_zero.rgs", """
STORY a PRIORITY 0.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING a:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "multiple_duplicates.rgs", """
STORY  a PRIORITY 1.
STORY  a PRIORITY 2.
ACTION run.
ACTION run.
EVENT  spotted ENVIRONMENT.
EVENT  spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")


# =============================================================================
# CATEGORY D — Semantic errors
# =============================================================================

def generate_semantic_errors():
    base = RGS / "semantic_errors"

    write(base / "undeclared_story.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING patrol:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "undeclared_event.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING a:
    WHEN exploded ENVIRONMENT:
        DO run.
""")
    write(base / "wrong_origin_event.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted MYSELF:
        DO run.
""")
    write(base / "undeclared_condition_if.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_hungry MYSELF:
        DO run.
""")
    write(base / "wrong_origin_condition.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired ENVIRONMENT:
        DO run.
""")
    write(base / "undeclared_action.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO fly.
""")
    write(base / "undeclared_condition_believe.rgs", """
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO BELIEVE is_hungry.
""")
    write(base / "undeclared_condition_forget.rgs", """
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO FORGET is_hungry.
""")


# =============================================================================
# CATEGORY E — Warnings
# =============================================================================

def generate_warnings():
    base = RGS / "warnings"

    write(base / "unused_action.rgs", """
ACTION run.
ACTION dance.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "unused_event.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
EVENT lost    ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(base / "unused_condition.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF:
        DO run.
""")
    write(base / "multiple_unused.rgs", """
ACTION run.
ACTION dance.
ACTION hide.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")


# =============================================================================
# CATEGORY F — Integration (source + expected output)
# =============================================================================

def generate_integration():
    src = RGS / "integration"

    # ── always_unconditional ──────────────────────────────────────────────────
    write(src / "always_unconditional.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(EXP / "always_unconditional.asl",
        "+spotted[source(percept)] : true <- run."
    )

    # ── always_conditional ────────────────────────────────────────────────────
    write(src / "always_conditional.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
        DO run.
""")
    write(EXP / "always_conditional.asl",
        "+spotted[source(percept)] : ~is_tired <- run."
    )

    # ── named_story_unconditional ─────────────────────────────────────────────
    write(src / "named_story_unconditional.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING a:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(EXP / "named_story_unconditional.asl",
        "+spotted[source(percept)] : story(a, 1) <- run."
    )

    # ── named_story_conditional ───────────────────────────────────────────────
    write(src / "named_story_conditional.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING a:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF:
        DO run.
""")
    write(EXP / "named_story_conditional.asl",
        "+spotted[source(percept)] : story(a, 1) & is_tired <- run."
    )

    # ── condition_not ─────────────────────────────────────────────────────────
    write(src / "condition_not.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
        DO run.
""")
    write(EXP / "condition_not.asl",
        "+spotted[source(percept)] : ~is_tired <- run."
    )

    # ── condition_and ─────────────────────────────────────────────────────────
    write(src / "condition_and.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_armed MYSELF AND NOT is_tired MYSELF:
        DO run.
""")
    write(EXP / "condition_and.asl",
        "+spotted[source(percept)] : is_armed & ~is_tired <- run."
    )

    # ── condition_or ─────────────────────────────────────────────────────────
    write(src / "condition_or.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF OR is_armed MYSELF:
        DO run.
""")
    write(EXP / "condition_or.asl",
        "+spotted[source(percept)] : is_tired | is_armed <- run."
    )

    # ── condition_or_with_story ───────────────────────────────────────────────
    write(src / "condition_or_with_story.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired MYSELF.
CONDITION is_armed MYSELF.
DURING a:
    WHEN spotted ENVIRONMENT IF is_tired MYSELF OR is_armed MYSELF:
        DO run.
""")
    write(EXP / "condition_or_with_story.asl",
        "+spotted[source(percept)] : story(a, 1) & (is_tired | is_armed) <- run."
    )

    # ── condition_parentheses ─────────────────────────────────────────────────
    write(src / "condition_parentheses.rgs", """
STORY a PRIORITY 1.
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION is_tired  MYSELF.
CONDITION door_open ENVIRONMENT.
CONDITION is_armed  MYSELF.
DURING a:
    WHEN spotted ENVIRONMENT IF (is_tired MYSELF OR door_open ENVIRONMENT) AND NOT is_armed MYSELF:
        DO run.
""")
    write(EXP / "condition_parentheses.asl",
        "+spotted[source(percept)] : story(a, 1) & (is_tired | door_open) & ~is_armed <- run."
    )

    # ── do_believe ────────────────────────────────────────────────────────────
    write(src / "do_believe.rgs", """
EVENT spotted ENVIRONMENT.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO BELIEVE is_armed.
""")
    write(EXP / "do_believe.asl",
        "+spotted[source(percept)] : true <- +is_armed."
    )

    # ── do_forget ─────────────────────────────────────────────────────────────
    write(src / "do_forget.rgs", """
EVENT lost ENVIRONMENT.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN lost ENVIRONMENT:
        DO FORGET is_armed.
""")
    write(EXP / "do_forget.asl",
        "+lost[source(percept)] : true <- -is_armed."
    )

    # ── multiple_actions ──────────────────────────────────────────────────────
    write(src / "multiple_actions.rgs", """
ACTION run.
ACTION hide.
ACTION dance.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run,
        DO hide,
        DO dance.
""")
    write(EXP / "multiple_actions.asl",
        "+spotted[source(percept)] : true <- run; hide; dance."
    )

    # ── priority_sorting ──────────────────────────────────────────────────────
    write(src / "priority_sorting.rgs", """
STORY low    PRIORITY 1.
STORY high   PRIORITY 3.
STORY medium PRIORITY 2.
ACTION run.
EVENT spotted ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT:
        DO run.
DURING low:
    WHEN spotted ENVIRONMENT:
        DO run.
DURING medium:
    WHEN spotted ENVIRONMENT:
        DO run.
DURING high:
    WHEN spotted ENVIRONMENT:
        DO run.
""")
    write(EXP / "priority_sorting.asl", "\n".join([
        "+spotted[source(percept)] : story(high, 3) <- run.",
        "+spotted[source(percept)] : story(medium, 2) <- run.",
        "+spotted[source(percept)] : story(low, 1) <- run.",
        "+spotted[source(percept)] : true <- run.",
    ]))

    # ── environment_origin ────────────────────────────────────────────────────
    write(src / "environment_origin.rgs", """
ACTION run.
EVENT spotted ENVIRONMENT.
CONDITION door_open ENVIRONMENT.
DURING ALWAYS:
    WHEN spotted ENVIRONMENT IF door_open ENVIRONMENT:
        DO run.
""")
    write(EXP / "environment_origin.asl",
        "+spotted[source(percept)] : door_open <- run."
    )

    # ── director_origin ───────────────────────────────────────────────────────
    write(src / "director_origin.rgs", """
ACTION run.
EVENT order DIRECTOR.
CONDITION approved DIRECTOR.
DURING ALWAYS:
    WHEN order DIRECTOR IF approved DIRECTOR:
        DO run.
""")
    write(EXP / "director_origin.asl",
        "+order[source(director)] : approved <- run."
    )

    # ── myself_origin ─────────────────────────────────────────────────────────
    write(src / "myself_origin.rgs", """
ACTION run.
EVENT ready MYSELF.
CONDITION is_armed MYSELF.
DURING ALWAYS:
    WHEN ready MYSELF IF is_armed MYSELF:
        DO run.
""")
    write(EXP / "myself_origin.asl",
        "+ready : is_armed <- run."
    )


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("Generating Category A — Valid syntax...")
    generate_valid()
    print("Generating Category B — Syntax errors...")
    generate_syntax_errors()
    print("Generating Category C — Declaration errors...")
    generate_declaration_errors()
    print("Generating Category D — Semantic errors...")
    generate_semantic_errors()
    print("Generating Category E — Warnings...")
    generate_warnings()
    print("Generating Category F — Integration...")
    generate_integration()
    print("\nDone. All test files generated.")