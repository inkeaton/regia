"""
Pass 1 tests: grammar parsing.

These tests verify that the Lark grammar correctly parses every
construct in the Regia v0.2 language. They do NOT check the AST
(that is Pass 3); they only verify that valid source code parses
without errors and that invalid source code raises exceptions.

Run with:  pytest tests/test_grammar.py -v
"""

import pytest
from lark import UnexpectedToken, UnexpectedCharacters

from regia.parser import parse


# == Base Element Declarations =================================================

class TestBaseElements:
    """Tests for ACTION, EVENT, and FACT declarations."""

    def test_action_simple(self) -> None:
        """A bare action declaration should parse."""
        parse("ACTION greet_back.")

    def test_action_with_params(self) -> None:
        """An action with parameter slots should parse."""
        parse("ACTION give_item(item, target).")

    def test_action_single_param(self) -> None:
        """An action with one parameter should parse."""
        parse("ACTION flee(direction).")

    def test_event_simple(self) -> None:
        """A bare event declaration should parse."""
        parse("EVENT fan_greets.")

    def test_event_with_self_origin(self) -> None:
        """An event with SELF origin should parse."""
        parse("EVENT internal_check SELF.")

    def test_event_with_environment_origin(self) -> None:
        """An event with ENVIRONMENT origin should parse."""
        parse("EVENT explosion ENVIRONMENT.")

    def test_fact_simple(self) -> None:
        """A bare fact declaration should parse."""
        parse("FACT happy.")

    def test_fact_with_params(self) -> None:
        """A parameterised fact should parse."""
        parse("FACT has_item(item).")

    def test_multiple_elements(self) -> None:
        """Multiple element declarations in sequence should parse."""
        parse("""
            ACTION greet.
            ACTION curse.
            EVENT fan_greets.
            FACT happy.
            FACT angry.
        """)


# == Playbook ==================================================================

class TestPlaybook:
    """Tests for PLAYBOOK definitions."""

    def test_simple_playbook(self) -> None:
        """A playbook with one unconditional WHEN block should parse."""
        parse("""
            PLAYBOOK Guard:
                WHEN alarm:
                    DO run_to_post.
        """)

    def test_playbook_with_conditions(self) -> None:
        """A playbook with IF/ELSE branches should parse."""
        parse("""
            PLAYBOOK Greeter:
                WHEN visitor_arrives:
                    IF happy:
                        DO greet.
                    IF angry:
                        DO curse.
                    ELSE:
                        DO ignore.
        """)

    def test_playbook_with_priority(self) -> None:
        """A playbook WHEN block with PRIORITY should parse."""
        parse("""
            PLAYBOOK Worker:
                WHEN boss_calls PRIORITY 7:
                    DO acknowledge.
        """)

    def test_playbook_with_signal(self) -> None:
        """A playbook with SIGNAL should parse."""
        parse("""
            PLAYBOOK Scout:
                WHEN enemy_spotted:
                    DO hide.
                    SIGNAL enemy_spotted.
        """)

    def test_playbook_signal_with_args(self) -> None:
        """A SIGNAL with arguments should parse."""
        parse("""
            PLAYBOOK Scout:
                WHEN enemy_spotted:
                    SIGNAL alert(location, threat_level).
        """)

    def test_playbook_multiple_when_blocks(self) -> None:
        """A playbook with multiple WHEN blocks should parse."""
        parse("""
            PLAYBOOK Citizen:
                WHEN greeted:
                    DO wave.
                WHEN attacked:
                    DO flee.
                WHEN asked_for_help PRIORITY 3:
                    DO help.
        """)

    def test_playbook_mixed_when_body(self) -> None:
        """A WHEN block with prefix DOs before IF branches should parse."""
        parse("""
            PLAYBOOK Logger:
                WHEN event_happens:
                    DO log_event.
                    IF important:
                        DO alert.
                    ELSE:
                        DO note.
        """)

    def test_playbook_special_actions(self) -> None:
        """Special DO actions (TELL, BROADCAST, etc.) should parse."""
        parse("""
            PLAYBOOK Messenger:
                WHEN news_received:
                    DO TELL(chief, news).
                    DO BROADCAST(alert).
                WHEN goal_set:
                    DO ACHIEVE(deliver_message).
                WHEN learned_fact:
                    DO BELIEVE(informed).
                WHEN forgot:
                    DO FORGET(old_info).
                WHEN debug:
                    DO PRINT("Found item", item, 42).
        """)

    def test_playbook_with_temper(self) -> None:
        """WHEN with TEMPER annotation should parse."""
        parse("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e TEMPER sympathy(0.8):
                    DO a.
        """)

    def test_playbook_with_temper_and_effects(self) -> None:
        """WHEN with TEMPER and EFFECTS should parse."""
        parse("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e TEMPER sympathy(0.8), aggressiveness(-0.5) EFFECTS fear(-0.05):
                    DO a.
        """)

    def test_playbook_with_priority_and_temper(self) -> None:
        """WHEN with both PRIORITY and TEMPER should parse."""
        parse("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e PRIORITY 5 TEMPER laziness(0.8) EFFECTS sympathy(0.05):
                    DO a.
        """)


# == Conditions ================================================================

class TestConditions:
    """Tests for boolean condition expressions inside IF blocks."""

    def test_simple_condition(self) -> None:
        """A bare fact check should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF happy:
                        DO a.
        """)

    def test_not_condition(self) -> None:
        """NOT negation should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF NOT angry:
                        DO a.
        """)

    def test_and_condition(self) -> None:
        """AND conjunction should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF happy AND healthy:
                        DO a.
        """)

    def test_or_condition(self) -> None:
        """OR disjunction should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF happy OR neutral:
                        DO a.
        """)

    def test_complex_condition(self) -> None:
        """A compound condition with NOT, AND, OR should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF happy AND NOT busy OR neutral:
                        DO a.
        """)

    def test_grouped_condition(self) -> None:
        """Parenthesised condition groups should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF (happy OR neutral) AND NOT busy:
                        DO a.
        """)

    def test_parameterised_fact_in_condition(self) -> None:
        """A fact with parameters in a condition should parse."""
        parse("""
            PLAYBOOK P:
                WHEN e:
                    IF has_item(sword) AND NOT poisoned:
                        DO a.
        """)


# == Plot ======================================================================

class TestPlot:
    """Tests for PLOT definitions."""

    def test_minimal_plot(self) -> None:
        """A minimal plot with one phase and one role should parse."""
        parse("""
            PLOT Quest.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        WORLD DO begin_quest.
        """)

    def test_plot_with_transitions(self) -> None:
        """A plot with phase transitions should parse."""
        parse("""
            PLOT Quest.
                PHASE asking INITIAL.
                PHASE searching.
                ROLE Hero.
                DURING asking:
                    TRANSITION TO searching WHEN accepted.
                    ON ENTER:
                        WORLD DO show_dialog.
        """)

    def test_transition_with_guard(self) -> None:
        """A transition with an IF condition guard should parse."""
        parse("""
            PLOT Quest.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    TRANSITION TO b WHEN timeout IF NOT quest_complete.
                    ON ENTER:
                        WORLD DO start.
        """)

    def test_on_enter_exit(self) -> None:
        """ON ENTER and ON EXIT blocks should parse."""
        parse("""
            PLOT Quest.
                PHASE main INITIAL.
                ROLE Hero.
                DURING main:
                    ON ENTER:
                        ASSIGN HeroBehaviour TO Hero.
                        WORLD DO start_music.
                    ON EXIT:
                        UNASSIGN HeroBehaviour FROM Hero.
                        WORLD DO stop_music.
        """)

    def test_plot_when_block(self) -> None:
        """A director-centric WHEN block inside a plot should parse."""
        parse("""
            PLOT Quest.
                PHASE main INITIAL.
                ROLE Hero.
                ROLE Villain.
                DURING main:
                    ON ENTER:
                        WORLD DO start.
                    WHEN emergency PRIORITY 9:
                        WORLD DO trigger_alarm.
                        Hero DO acknowledge.
                        Villain DO flee.
        """)

    def test_plot_when_with_conditions(self) -> None:
        """A plot WHEN block with IF/ELSE should parse."""
        parse("""
            PLOT Quest.
                PHASE main INITIAL.
                ROLE Hero.
                DURING main:
                    ON ENTER:
                        WORLD DO start.
                    WHEN player_choice:
                        IF heroic:
                            Hero DO fight.
                            WORLD DO play_battle_music.
                        ELSE:
                            Hero DO flee.
        """)

    def test_during_plot_wide(self) -> None:
        """DURING PLOT: (phase-independent) block should parse."""
        parse("""
            PLOT Quest.
                PHASE a INITIAL.
                PHASE b.
                ROLE Hero.
                DURING PLOT:
                    WHEN emergency PRIORITY 9:
                        WORLD DO evacuate.
                DURING a:
                    TRANSITION TO b WHEN trigger.
                    ON ENTER:
                        WORLD DO start.
        """)

    def test_role_do_with_special_action(self) -> None:
        """A role directive using a special action should parse."""
        parse("""
            PLOT Quest.
                PHASE main INITIAL.
                ROLE Hero.
                DURING main:
                    ON ENTER:
                        Hero DO TELL(companion, lets_go).
                        WORLD DO BROADCAST(quest_started).
        """)

    def test_world_do_with_args(self) -> None:
        """WORLD DO with action arguments should parse."""
        parse("""
            PLOT Quest.
                PHASE main INITIAL.
                ROLE Hero.
                DURING main:
                    ON ENTER:
                        WORLD DO spawn_enemies(3, location_a).
        """)

    def test_multiple_phases_and_roles(self) -> None:
        """A plot with multiple phases and roles should parse."""
        parse("""
            PLOT Concert.
                PHASE backstage INITIAL.
                PHASE performing.
                PHASE aftermath.
                ROLE Singer.
                ROLE AudienceMember.
                ROLE StageManager.
                DURING backstage:
                    TRANSITION TO performing WHEN time_to_start.
                    ON ENTER:
                        ASSIGN SingerBackstage TO Singer.
                        WORLD DO prepare_stage.
                    ON EXIT:
                        UNASSIGN SingerBackstage FROM Singer.
                DURING performing:
                    TRANSITION TO aftermath WHEN song_ends.
                    ON ENTER:
                        ASSIGN SingerOnStage TO Singer.
        """)


# == Full Example ==============================================================

class TestFullExample:
    """Tests the complete worked example from the language spec."""

    FULL_EXAMPLE = """
        # Base Elements
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

        # Playbooks
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

        # Plot
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

                TRANSITION TO performing WHEN time_to_start.

                ON ENTER:
                    ASSIGN SingerInBackstage TO Singer.
                    WORLD DO add_waiting_for_concert.

                ON EXIT:
                    UNASSIGN SingerInBackstage FROM Singer.
                    WORLD DO announce_concert.

            DURING performing:

                TRANSITION TO aftermath WHEN song_ends IF audience_satisfied.

                ON ENTER:
                    ASSIGN SingerOnStage TO Singer.
                    WORLD DO start_music.

                ON EXIT:
                    UNASSIGN SingerOnStage FROM Singer.
    """

    def test_full_example_parses(self) -> None:
        """The complete spec example should parse without errors."""
        tree = parse(self.FULL_EXAMPLE)
        assert tree is not None
        assert tree.data == "program"

    def test_full_example_child_count(self) -> None:
        """The full example should have the right number of top-level items.

        11 actions + 6 events + 3 facts + 2 playbooks + 1 plot = 23
        """
        tree = parse(self.FULL_EXAMPLE)
        # With ? inlining, program's children are direct nodes
        assert len(tree.children) == 23

    def test_full_example_has_plot(self) -> None:
        """The full example should contain exactly one plot_def."""
        tree = parse(self.FULL_EXAMPLE)
        plots = [c for c in tree.children if hasattr(c, "data") and c.data == "plot_def"]
        assert len(plots) == 1

    def test_full_example_has_playbooks(self) -> None:
        """The full example should contain exactly two playbook_defs."""
        tree = parse(self.FULL_EXAMPLE)
        pbs = [c for c in tree.children if hasattr(c, "data") and c.data == "playbook_def"]
        assert len(pbs) == 2


# == Syntax Errors =============================================================

class TestSyntaxErrors:
    """Tests that invalid syntax is correctly rejected."""

    def test_missing_period(self) -> None:
        """A missing period after a declaration should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("ACTION greet")

    def test_missing_colon_after_playbook(self) -> None:
        """A missing colon after PLAYBOOK name should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("""
                PLAYBOOK Guard
                    WHEN alarm:
                        DO run.
            """)

    def test_empty_when_body(self) -> None:
        """A WHEN block with no body should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("""
                PLAYBOOK Guard:
                    WHEN alarm:
            """)

    def test_missing_plot_name(self) -> None:
        """PLOT without a name should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("PLOT .")

    def test_do_without_action(self) -> None:
        """DO without an action name should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("""
                PLAYBOOK P:
                    WHEN e:
                        DO .
            """)

    def test_empty_program(self) -> None:
        """An empty program should error (at least one item required)."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("")

    def test_unclosed_arg_list(self) -> None:
        """An unclosed parenthesis in an argument list should error."""
        with pytest.raises((UnexpectedToken, UnexpectedCharacters)):
            parse("ACTION give(item.")
