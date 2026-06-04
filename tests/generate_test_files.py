"""
Generates all RegiaScript v2 test fixture files.
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
# CATEGORY A - Valid syntax
# =============================================================================

def generate_valid():
    base = RGS / "valid"

    write(base / "default_story_only.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "named_story_no_phases.rgs", """
STORY combat PRIORITY 2.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Guard:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "named_story_with_phases.rgs", """
STORY quest PRIORITY 1.
    ACTION complete.
    EVENT finished ENVIRONMENT.
    PHASE active.
    PHASE done.
    AGENT Hero:
        DURING active:
            WHEN finished ENVIRONMENT:
                ENTER done.
""")

    write(base / "multiple_phases.rgs", """
STORY quest PRIORITY 1.
    EVENT e ENVIRONMENT.
    ACTION a.
    PHASE p1.
    PHASE p2.
    PHASE p3.
    PHASE p4.
    AGENT Hero:
        DURING p1:
            WHEN e ENVIRONMENT:
                ENTER p2.
        DURING p2:
            WHEN e ENVIRONMENT:
                ENTER p3.
        DURING p3:
            WHEN e ENVIRONMENT:
                ENTER p4.
        DURING p4:
            WHEN e ENVIRONMENT:
                DO a.
""")

    write(base / "multiple_agents.rgs", """
STORY quest PRIORITY 1.
    ACTION reward.
    EVENT done ENVIRONMENT.
    PHASE active.
    PHASE complete.
    AGENT Citizen:
        DURING active:
            WHEN done ENVIRONMENT:
                DO reward,
                ENTER complete.
    AGENT Player:
        DURING active:
            WHEN done ENVIRONMENT:
                ENTER complete.
""")

    write(base / "during_always_in_named_story.rgs", """
STORY quest PRIORITY 1.
    ACTION flee.
    EVENT danger ENVIRONMENT.
    PHASE active.
    PHASE done.
    AGENT Hero:
        DURING ALWAYS:
            WHEN danger ENVIRONMENT:
                DO flee.
        DURING active:
            WHEN danger ENVIRONMENT:
                ENTER done.
""")

    write(base / "all_origins.rgs", """
STORY quest PRIORITY 1.
    ACTION a.
    EVENT env_event  ENVIRONMENT.
    EVENT dir_event  DIRECTOR.
    EVENT self_event MYSELF.
    EVENT play_event PLAYER.
    EVENT time_event TIMER.
    CONDITION env_cond  ENVIRONMENT.
    CONDITION dir_cond  DIRECTOR.
    CONDITION self_cond MYSELF.
    PHASE p1.
    AGENT Hero:
        DURING p1:
            WHEN env_event  ENVIRONMENT IF env_cond  ENVIRONMENT: DO a.
            WHEN dir_event  DIRECTOR    IF dir_cond  DIRECTOR:    DO a.
            WHEN self_event MYSELF      IF self_cond MYSELF:      DO a.
            WHEN play_event PLAYER:                               DO a.
            WHEN time_event TIMER:                                DO a.
""")

    write(base / "condition_not.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
                DO run.
""")

    write(base / "condition_and.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_armed MYSELF AND NOT is_tired MYSELF:
                DO run.
""")

    write(base / "condition_or.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_tired MYSELF OR is_armed MYSELF:
                DO run.
""")

    write(base / "condition_parentheses.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired  MYSELF.
    CONDITION is_armed  MYSELF.
    CONDITION door_open ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF (is_tired MYSELF OR door_open ENVIRONMENT) AND NOT is_armed MYSELF:
                DO run.
""")

    write(base / "do_believe_forget.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    EVENT lost    ENVIRONMENT.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO BELIEVE is_armed.
            WHEN lost ENVIRONMENT:
                DO FORGET is_armed.
""")

    write(base / "multiple_actions_in_do.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    ACTION hide.
    ACTION dance.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run,
                DO hide,
                DO dance.
""")

    write(base / "agent_local_declarations.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        ACTION local_action.
        CONDITION local_cond MYSELF.
        DURING active:
            WHEN spotted ENVIRONMENT IF local_cond MYSELF:
                DO local_action.
""")

    write(base / "multiple_stories.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.

STORY combat PRIORITY 2.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Guard:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "doc_comments.rgs", """
# @NAME: Main quest
# @MEANING: The primary narrative
STORY quest PRIORITY 1.
    # @NAME: Finish event
    EVENT done ENVIRONMENT.
    ACTION complete.
    # @NAME: Active phase
    PHASE active.
    PHASE finished.
    # @NAME: Hero agent
    AGENT Hero:
        # @NAME: Completion plan
        DURING active:
            WHEN done ENVIRONMENT:
                DO complete,
                ENTER finished.
""")

    write(base / "plain_comments.rgs", """
# This is a plain comment
STORY DEFAULT. # inline
    AGENT Guard:
        ACTION patrol.
        # another comment
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol. # end comment
""")

    write(base / "flat_formatting.rgs", """
STORY DEFAULT.
AGENT Guard:
ACTION patrol.
EVENT idle MYSELF.
DURING ALWAYS:
WHEN idle MYSELF: DO patrol.
""")

    write(base / "enter_in_always_block.rgs", """
STORY quest PRIORITY 1.
    ACTION flee.
    EVENT danger ENVIRONMENT.
    EVENT killed ENVIRONMENT.
    PHASE active.
    PHASE failed.
    AGENT Hero:
        DURING ALWAYS:
            WHEN killed ENVIRONMENT:
                ENTER failed.
        DURING active:
            WHEN danger ENVIRONMENT:
                DO flee.
""")


# =============================================================================
# CATEGORY B - Syntax errors
# =============================================================================

def generate_syntax_errors():
    base = RGS / "syntax_errors"

    write(base / "missing_story_keyword.rgs", """
DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "named_story_missing_priority_keyword.rgs", """
STORY quest 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "named_story_missing_priority_number.rgs", """
STORY quest PRIORITY.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "named_story_missing_period.rgs", """
STORY quest PRIORITY 1
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "default_story_missing_period.rgs", """
STORY DEFAULT
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "agent_missing_name.rgs", """
STORY DEFAULT.
    AGENT:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "agent_missing_colon.rgs", """
STORY DEFAULT.
    AGENT Guard
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "phase_missing_name.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "phase_missing_period.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "action_missing_name.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "action_missing_period.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "event_missing_origin.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "during_missing_phase.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "during_missing_colon.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "during_no_when_blocks.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "when_missing_event.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN MYSELF:
                DO patrol.
""")

    write(base / "when_missing_origin.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle:
                DO patrol.
""")

    write(base / "when_missing_colon.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF
                DO patrol.
""")

    write(base / "when_if_no_condition.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF IF:
                DO patrol.
""")

    write(base / "do_missing_action.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO.
""")

    write(base / "do_believe_missing_name.rgs", """
STORY DEFAULT.
    AGENT Guard:
        EVENT idle MYSELF.
        CONDITION armed MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO BELIEVE.
""")

    write(base / "enter_missing_phase.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                ENTER.
""")

    write(base / "unclosed_parenthesis.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION tired MYSELF.
    CONDITION armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF (tired MYSELF OR armed MYSELF:
                DO run.
""")

    write(base / "and_no_right_operand.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION tired MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF tired MYSELF AND:
                DO run.
""")


# =============================================================================
# CATEGORY C - Declaration errors
# =============================================================================

def generate_declaration_errors():
    base = RGS / "declaration_errors"

    write(base / "duplicate_story.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.

STORY quest PRIORITY 2.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "duplicate_default_story.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.

STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")

    write(base / "priority_zero.rgs", """
STORY quest PRIORITY 0.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    AGENT Hero:
        DURING ALWAYS:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "duplicate_phase.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    PHASE active.
    PHASE done.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                ENTER done.
""")

    write(base / "duplicate_agent_in_story.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "duplicate_story_action.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "duplicate_story_event.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")


# =============================================================================
# CATEGORY D - Semantic errors
# =============================================================================

def generate_semantic_errors():
    base = RGS / "semantic_errors"

    write(base / "undeclared_event.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN exploded ENVIRONMENT:
                DO run.
""")

    write(base / "wrong_origin_event.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted MYSELF:
                DO run.
""")

    write(base / "undeclared_action.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO fly.
""")

    write(base / "undeclared_condition_if.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_hungry MYSELF:
                DO run.
""")

    write(base / "wrong_origin_condition.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_tired ENVIRONMENT:
                DO run.
""")

    write(base / "undeclared_condition_believe.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO BELIEVE is_hungry.
""")

    write(base / "undeclared_condition_forget.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO FORGET is_hungry.
""")

    write(base / "undeclared_phase_in_during.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING missing_phase:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "undeclared_phase_in_enter.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                ENTER missing_phase.
""")

    write(base / "enter_in_default_story.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                ENTER some_phase.
""")


# =============================================================================
# CATEGORY E - Warnings
# =============================================================================

def generate_warnings():
    base = RGS / "warnings"

    write(base / "unused_action.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    ACTION dance.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "unused_event.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    EVENT lost    ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")

    write(base / "unused_condition.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_tired MYSELF:
                DO run.
""")

    write(base / "multiple_unused.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    ACTION dance.
    ACTION hide.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")


# =============================================================================
# CATEGORY F - Integration (source + expected output)
# =============================================================================

def generate_integration():
    src = RGS / "integration"

    # ── default_story_plan ────────────────────────────────────────────────────
    write(src / "default_story_plan.rgs", """
STORY DEFAULT.
    AGENT Guard:
        ACTION patrol.
        EVENT idle MYSELF.
        DURING ALWAYS:
            WHEN idle MYSELF:
                DO patrol.
""")
    write(EXP / "default_story_plan_Guard.asl",
        "+idle : true <- patrol."
    )

    # ── named_story_unconditional ─────────────────────────────────────────────
    write(src / "named_story_unconditional.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")
    write(EXP / "named_story_unconditional_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active <- run."
    )

    # ── named_story_always_plan ───────────────────────────────────────────────
    write(src / "named_story_always_plan.rgs", """
STORY quest PRIORITY 1.
    ACTION flee.
    EVENT danger ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING ALWAYS:
            WHEN danger ENVIRONMENT:
                DO flee.
""")
    write(EXP / "named_story_always_plan_Hero.asl",
        "+danger[source(percept)] : story(quest, 1) <- flee."
    )

    # ── condition_not ─────────────────────────────────────────────────────────
    write(src / "condition_not.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF NOT is_tired MYSELF:
                DO run.
""")
    write(EXP / "condition_not_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active & ~is_tired <- run."
    )

    # ── condition_and ─────────────────────────────────────────────────────────
    write(src / "condition_and.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_armed MYSELF AND NOT is_tired MYSELF:
                DO run.
""")
    write(EXP / "condition_and_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active & is_armed & ~is_tired <- run."
    )

    # ── condition_or ─────────────────────────────────────────────────────────
    write(src / "condition_or.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired MYSELF.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF is_tired MYSELF OR is_armed MYSELF:
                DO run.
""")
    write(EXP / "condition_or_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active & (is_tired | is_armed) <- run."
    )

    # ── condition_parentheses ─────────────────────────────────────────────────
    write(src / "condition_parentheses.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    CONDITION is_tired  MYSELF.
    CONDITION door_open ENVIRONMENT.
    CONDITION is_armed  MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT IF (is_tired MYSELF OR door_open ENVIRONMENT) AND NOT is_armed MYSELF:
                DO run.
""")
    write(EXP / "condition_parentheses_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active & (is_tired | door_open) & ~is_armed <- run."
    )

    # ── do_believe ────────────────────────────────────────────────────────────
    write(src / "do_believe.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO BELIEVE is_armed.
""")
    write(EXP / "do_believe_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active <- +is_armed."
    )

    # ── do_forget ─────────────────────────────────────────────────────────────
    write(src / "do_forget.rgs", """
STORY quest PRIORITY 1.
    EVENT lost ENVIRONMENT.
    CONDITION is_armed MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN lost ENVIRONMENT:
                DO FORGET is_armed.
""")
    write(EXP / "do_forget_Hero.asl",
        "+lost[source(percept)] : story(quest, 1) & active <- -is_armed."
    )

    # ── multiple_actions ──────────────────────────────────────────────────────
    write(src / "multiple_actions.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    ACTION hide.
    ACTION dance.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run,
                DO hide,
                DO dance.
""")
    write(EXP / "multiple_actions_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active <- run; hide; dance."
    )

    # ── environment_origin ────────────────────────────────────────────────────
    write(src / "environment_origin.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")
    write(EXP / "environment_origin_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active <- run."
    )

    # ── director_origin ───────────────────────────────────────────────────────
    write(src / "director_origin.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT order DIRECTOR.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN order DIRECTOR:
                DO run.
""")
    write(EXP / "director_origin_Hero.asl",
        "+order[source(director)] : story(quest, 1) & active <- run."
    )

    # ── player_origin ─────────────────────────────────────────────────────────
    write(src / "player_origin.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT accepted PLAYER.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN accepted PLAYER:
                DO run.
""")
    write(EXP / "player_origin_Hero.asl",
        "+accepted[source(player)] : story(quest, 1) & active <- run."
    )

    # ── timer_origin ──────────────────────────────────────────────────────────
    write(src / "timer_origin.rgs", """
STORY quest PRIORITY 1.
    ACTION give_up.
    EVENT expired TIMER.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN expired TIMER:
                DO give_up.
""")
    write(EXP / "timer_origin_Hero.asl",
        "+expired[source(timer)] : story(quest, 1) & active <- give_up."
    )

    # ── myself_origin ─────────────────────────────────────────────────────────
    write(src / "myself_origin.rgs", """
STORY quest PRIORITY 1.
    ACTION run.
    EVENT ready MYSELF.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN ready MYSELF:
                DO run.
""")
    write(EXP / "myself_origin_Hero.asl",
        "+ready : story(quest, 1) & active <- run."
    )

    # ── priority_sorting ──────────────────────────────────────────────────────
    write(src / "priority_sorting.rgs", """
STORY low    PRIORITY 1.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.

STORY high PRIORITY 3.
    ACTION run.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        DURING active:
            WHEN spotted ENVIRONMENT:
                DO run.
""")
    write(EXP / "priority_sorting_Hero.asl", "\n".join([
        "+spotted[source(percept)] : story(high, 3) & active <- run.",
        "+spotted[source(percept)] : story(low, 1) & active <- run.",
    ]))

    # ── enter_phase ───────────────────────────────────────────────────────────
    write(src / "enter_phase.rgs", """
STORY quest PRIORITY 1.
    EVENT done ENVIRONMENT.
    PHASE active.
    PHASE complete.
    AGENT Hero:
        DURING active:
            WHEN done ENVIRONMENT:
                ENTER complete.
""")
    write(EXP / "enter_phase_Hero.asl",
        "+done[source(percept)] : story(quest, 1) & active <- !enter_quest_complete."
    )

    # ── agent_local_declarations ──────────────────────────────────────────────
    write(src / "agent_local_declarations.rgs", """
STORY quest PRIORITY 1.
    EVENT spotted ENVIRONMENT.
    PHASE active.
    AGENT Hero:
        ACTION local_run.
        CONDITION local_cond MYSELF.
        DURING active:
            WHEN spotted ENVIRONMENT IF local_cond MYSELF:
                DO local_run.
""")
    write(EXP / "agent_local_declarations_Hero.asl",
        "+spotted[source(percept)] : story(quest, 1) & active & local_cond <- local_run."
    )

    # ── multi_agent ───────────────────────────────────────────────────────────
    write(src / "multi_agent.rgs", """
STORY quest PRIORITY 1.
    ACTION reward.
    ACTION celebrate.
    EVENT done ENVIRONMENT.
    PHASE active.
    PHASE complete.
    AGENT Citizen:
        DURING active:
            WHEN done ENVIRONMENT:
                DO reward,
                ENTER complete.
    AGENT Player:
        DURING active:
            WHEN done ENVIRONMENT:
                DO celebrate,
                ENTER complete.
""")
    write(EXP / "multi_agent_Citizen.asl", "\n".join([
        "+done[source(percept)] : story(quest, 1) & active <- reward; !enter_quest_complete.",
    ]))
    write(EXP / "multi_agent_Player.asl", "\n".join([
        "+done[source(percept)] : story(quest, 1) & active <- celebrate; !enter_quest_complete.",
    ]))


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("Generating Category A - Valid syntax...")
    generate_valid()
    print("Generating Category B - Syntax errors...")
    generate_syntax_errors()
    print("Generating Category C - Declaration errors...")
    generate_declaration_errors()
    print("Generating Category D - Semantic errors...")
    generate_semantic_errors()
    print("Generating Category E - Warnings...")
    generate_warnings()
    print("Generating Category F - Integration...")
    generate_integration()
    print("\nDone. All test files generated.")