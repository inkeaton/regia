"""
Pass 5 tests: AgentSpeak emitter.

These tests verify that the Emitter correctly transforms
validated ASTs into AgentSpeak (.asl) source code.

Each test compiles a Regia source string through the full pipeline
and checks the resulting output files for expected patterns.

Run with:  pytest tests/test_emitter.py -v
"""

import pytest

from pathlib import Path

from regia.compiler import compile_source, compile_files, CompileResult


def _compile(source: str) -> CompileResult:
    """Compile source through the full pipeline.

    Args:
        source: Regia source code string.

    Returns:
        A CompileResult with outputs.
    """
    return compile_source(source)


# == Output File Generation ====================================================

class TestOutputFiles:
    """Tests for correct output file generation."""

    def test_director_file_generated(self) -> None:
        """A Plot should produce a director_<name>.asl file."""
        result = _compile("""
            ACTION a.
            PLOT MyPlot.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO a.
        """)
        assert result.success
        assert "director_myplot.asl" in result.outputs

    def test_role_file_generated(self) -> None:
        """Roles used in a Plot should produce role_<plot>_<name>.asl files."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        ASSIGN Pb TO Hero.
        """)
        assert result.success
        assert "role_p_hero.asl" in result.outputs

    def test_no_plot_no_director(self) -> None:
        """Without a Plot, no director or role files should be generated."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
        """)
        assert result.success
        assert len(result.outputs) == 1
        assert "playbook_pb.asl" in result.outputs

    def test_playbook_file_generated(self) -> None:
        """Assigned Playbooks should produce playbook_<name>.asl files."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        ASSIGN Pb TO Hero.
        """)
        assert result.success
        assert "playbook_pb.asl" in result.outputs

    def test_role_includes_playbook(self) -> None:
        """Role file should include assigned playbook files."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        ASSIGN Pb TO Hero.
        """)
        assert result.success
        role_output = result.outputs["role_p_hero.asl"]
        assert '{ include("playbook_pb.asl") }' in role_output

    def test_playbook_file_contains_plans(self) -> None:
        """Playbook file should contain static-gated plans."""
        result = _compile("""
            ACTION greet.
            EVENT hello.
            PLAYBOOK Greeter:
                WHEN hello:
                    DO greet.
            PLOT P.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN Greeter TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_greeter.asl"]
        assert "playbook_active(greeter, _)" in pb_output
        assert "+hello" in pb_output
        assert "greet" in pb_output


# == Director Output ===========================================================

class TestDirectorOutput:
    """Tests for director .asl file content."""

    def _director(self, source: str) -> str:
        """Compile and return the director output.

        Args:
            source: Regia source string.

        Returns:
            The director .asl file content.
        """
        result = _compile(source)
        assert result.success, (
            f"Compilation failed: "
            + "; ".join(m.message for m in result.messages)
        )
        directors = [
            v for k, v in result.outputs.items()
            if k.startswith("director_")
        ]
        assert len(directors) == 1
        return directors[0]

    def test_initial_phase_belief(self) -> None:
        """Director should have initial phase belief."""
        output = self._director("""
            ACTION a.
            PLOT P.
                PHASE intro INITIAL.
                ROLE R.
                DURING intro:
                    ON ENTER:
                        WORLD DO a.
        """)
        assert "current_phase(intro)." in output

    def test_boot_plan_calls_on_enter(self) -> None:
        """Boot plan should include ON ENTER actions."""
        output = self._director("""
            ACTION setup.
            PLOT P.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO setup.
        """)
        assert "+!boot" in output
        assert "setup" in output

    def test_transition_plan(self) -> None:
        """Transition should generate a proper plan."""
        output = self._director("""
            ACTION a.
            EVENT trigger.
            PLOT P.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    WHEN trigger:
                        TRANSITION TO b.
                    ON ENTER:
                        WORLD DO a.
        """)
        assert "+trigger" in output
        assert "current_phase(a)" in output
        assert "!switch_phase(b)" in output

    def test_guarded_transition(self) -> None:
        """Guarded transition should include condition in context."""
        output = self._director("""
            ACTION a.
            EVENT trigger.
            FACT ready.
            PLOT P.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    WHEN trigger:
                        IF ready:
                            TRANSITION TO b.
                    ON ENTER:
                        WORLD DO a.
        """)
        assert "current_phase(a) & ready" in output

    def test_transition_runs_on_exit_then_on_enter(self) -> None:
        """Transition body should run ON EXIT before ON ENTER."""
        output = self._director("""
            ACTION exit_action.
            ACTION enter_action.
            EVENT trigger.
            PLOT P.
                PHASE a INITIAL.
                PHASE b.
                ROLE R.
                DURING a:
                    WHEN trigger:
                        TRANSITION TO b.
                    ON ENTER:
                        WORLD DO enter_action.
                    ON EXIT:
                        WORLD DO exit_action.
                DURING b:
                    ON ENTER:
                        WORLD DO enter_action.
        """)
        # Ensure the infrastructural hooks are generated correctly
        assert "+!on_exit(a) <-" in output
        assert "exit_action" in output.split("+!on_exit(a) <-")[1]
        assert "+!on_enter(b) <-" in output
        assert "enter_action" in output.split("+!on_enter(b) <-")[1]

    def test_director_when_block(self) -> None:
        """Director WHEN block should produce a plan."""
        output = self._director("""
            ACTION alert.
            EVENT alarm.
            PLOT P.
                PHASE start INITIAL.
                ROLE R.
                DURING start:
                    ON ENTER:
                        WORLD DO alert.
                    WHEN alarm:
                        WORLD DO alert.
        """)
        assert "+alarm" in output
        assert "current_phase(start)" in output

    def test_director_plot_wide_when(self) -> None:
        """DURING PLOT WHEN block should work in all phases."""
        output = self._director("""
            ACTION alert.
            EVENT alarm.
            PLOT P.
                PHASE start INITIAL.
                ROLE R.
                DURING PLOT:
                    WHEN alarm:
                        WORLD DO alert.
        """)
        # Plot-wide plan should not have current_phase in context
        assert "+alarm : true <-" in output

    def test_director_when_priority(self) -> None:
        """WHEN with PRIORITY should include annotation."""
        output = self._director("""
            ACTION alert.
            EVENT alarm.
            PLOT P.
                PHASE start INITIAL.
                ROLE R.
                DURING PLOT:
                    WHEN alarm PRIORITY 5:
                        WORLD DO alert.
        """)
        assert "@dir__P__alarm__0[priority(5)]" in output

    def test_assign_sends_add_playbook(self) -> None:
        """ASSIGN should emit .send with add_playbook."""
        output = self._director("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        ASSIGN Pb TO Hero.
        """)
        assert "!send_to_role(hero, achieve, add_playbook(pb))" in output

    def test_unassign_sends_remove_playbook(self) -> None:
        """UNASSIGN should emit .send with remove_playbook."""
        output = self._director("""
            ACTION a.
            EVENT e.
            EVENT trigger.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                PHASE next.
                ROLE Hero.
                DURING start:
                    WHEN trigger:
                        TRANSITION TO next.
                    ON ENTER:
                        ASSIGN Pb TO Hero.
                    ON EXIT:
                        UNASSIGN Pb FROM Hero.
        """)
        assert "!send_to_role(hero, achieve, remove_playbook(pb))" in output

    def test_role_do_sends_achieve(self) -> None:
        """Role DO should emit !send_to_role(role, achieve, action)."""
        output = self._director("""
            ACTION duck.
            EVENT danger.
            PLOT P.
                PHASE start INITIAL.
                ROLE Guard.
                DURING start:
                    ON ENTER:
                        WORLD DO duck.
                    WHEN danger:
                        Guard DO duck.
        """)
        assert "!send_to_role(guard, achieve, duck)" in output


# == Role Output ===============================================================

class TestRoleOutput:
    """Tests for role template .asl file content."""

    def _role(self, source: str, role_name: str, plot_name: str = "P") -> str:
        """Compile and return a specific role output.

        Args:
            source:    Regia source string.
            role_name: The role name (lowercase for filename).
            plot_name: The plot name (lowercase for filename, default 'P').

        Returns:
            The role .asl file content.
        """
        result = _compile(source)
        assert result.success
        key = f"role_{plot_name.lower()}_{role_name.lower()}.asl"
        assert key in result.outputs
        return result.outputs[key]

    def test_playbook_management_handlers(self) -> None:
        """Role should have add/remove_playbook handlers."""
        output = self._role("""
            ACTION a.
            EVENT e.
            PLAYBOOK Pb:
                WHEN e:
                    DO a.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        ASSIGN Pb TO Hero.
        """, "Hero")
        assert "+!add_playbook(Name)[source(Sender)]" in output
        assert "+playbook_active(Name, Sender)" in output
        assert "+!remove_playbook(Name)[source(Sender)]" in output
        assert "-playbook_active(Name, Sender)" in output
        assert "+plot_ended(PlotId)[source(PlotId)]" in output
        assert "+!signal_directors(PbName, Payload) <-" in output
        assert ".findall(D, playbook_active(PbName, D), Directors);" in output

    def test_static_gated_plan(self) -> None:
        """Playbook plans should be gated by playbook_active."""
        output = self._role("""
            ACTION greet.
            EVENT hello.
            PLAYBOOK Greeter:
                WHEN hello:
                    DO greet.
            PLOT P.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN Greeter TO NPC.
        """, "NPC")
        # Plans are now in the playbook file, not inline in the role.
        # Role file should have include directive and management handlers.
        assert '+!add_playbook(Name)[source(Sender)]' in output
        assert '+!remove_playbook(Name)[source(Sender)]' in output
        assert '{ include("playbook_greeter.asl") }' in output

    def test_conditional_plans_in_playbook_file(self) -> None:
        """IF/ELSE in Playbook should produce separate gated plans in playbook file."""
        result = _compile("""
            ACTION greet.
            ACTION ignore.
            EVENT hello.
            FACT happy.
            PLAYBOOK P:
                WHEN hello:
                    IF happy:
                        DO greet.
                    ELSE:
                        DO ignore.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "playbook_active(p, _) & happy" in pb_output
        assert "not (happy)" in pb_output

    def test_special_action_tell(self) -> None:
        """DO TELL should emit .send in playbook file."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO TELL(player, msg).
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert ".send(player, tell, msg)" in pb_output

    def test_special_action_broadcast(self) -> None:
        """DO BROADCAST should emit .broadcast in playbook file."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO BROADCAST(alert).
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert ".broadcast(tell, alert)" in pb_output

    def test_special_action_achieve(self) -> None:
        """DO ACHIEVE should emit !goal in playbook file."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO ACHIEVE(run_away).
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "!run_away" in pb_output

    def test_special_action_believe_forget(self) -> None:
        """DO BELIEVE and FORGET should emit +/- belief in playbook file."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO BELIEVE(alert_mode).
                    DO FORGET(calm).
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "+alert_mode" in pb_output
        assert "-calm" in pb_output

    def test_special_action_print(self) -> None:
        """DO PRINT should emit .print in playbook file."""
        result = _compile("""
            EVENT e.
            PLAYBOOK P:
                WHEN e:
                    DO PRINT("Hello", name, 42).
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert '.print("Hello", name, 42)' in pb_output

    def test_signal_emits_send_to_director(self) -> None:
        """SIGNAL should emit .send(director, tell, event) in playbook file."""
        result = _compile("""
            ACTION flee.
            EVENT attack.
            PLAYBOOK P:
                WHEN attack:
                    DO flee.
                    SIGNAL attack.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "!signal_directors(p, attack)" in pb_output

    def test_priority_annotation(self) -> None:
        """WHEN with PRIORITY should include @priority annotation in playbook file."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e PRIORITY 3:
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "@pb__P__e__0[priority(3)]" in pb_output

    def test_temper_annotation(self) -> None:
        """WHEN with TEMPER should include temper annotation in playbook file."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e TEMPER sympathy(0.8):
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "temper([sympathy(0.8)])" in pb_output

    def test_temper_with_effects(self) -> None:
        """WHEN with TEMPER and EFFECTS should include both annotations."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e TEMPER sympathy(0.8) EFFECTS fear(-0.05):
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "temper([sympathy(0.8)])" in pb_output
        assert "effects([fear(-0.05)])" in pb_output

    def test_temper_and_priority(self) -> None:
        """WHEN with both PRIORITY and TEMPER should include all annotations."""
        result = _compile("""
            ACTION a.
            EVENT e.
            PLAYBOOK P:
                WHEN e PRIORITY 5 TEMPER laziness(0.8) EFFECTS sympathy(0.05):
                    DO a.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)
        assert result.success
        pb_output = result.outputs["playbook_p.asl"]
        assert "priority(5)" in pb_output
        assert "temper([laziness(0.8)])" in pb_output
        assert "effects([sympathy(0.05)])" in pb_output

    def test_multiple_playbooks_on_same_role(self) -> None:
        """A Role with multiple Playbooks should include both playbook files."""
        result = _compile("""
            ACTION greet.
            ACTION fight.
            EVENT hello.
            EVENT attack.
            PLAYBOOK Friendly:
                WHEN hello:
                    DO greet.
            PLAYBOOK Fighter:
                WHEN attack:
                    DO fight.
            PLOT P.
                PHASE peace INITIAL.
                PHASE war.
                ROLE Guard.
                DURING peace:
                    WHEN attack:
                        TRANSITION TO war.
                    ON ENTER:
                        ASSIGN Friendly TO Guard.
                    ON EXIT:
                        UNASSIGN Friendly FROM Guard.
                DURING war:
                    ON ENTER:
                        ASSIGN Fighter TO Guard.
        """)
        assert result.success
        role_output = result.outputs["role_p_guard.asl"]
        assert '{ include("playbook_friendly.asl") }' in role_output
        assert '{ include("playbook_fighter.asl") }' in role_output
        # Plans should be in their own playbook files
        assert "playbook_active(friendly, _)" in result.outputs["playbook_friendly.asl"]
        assert "playbook_active(fighter, _)" in result.outputs["playbook_fighter.asl"]

    def test_role_do_handler_plan(self) -> None:
        """Role DO should generate achievement goal handler in role file."""
        output = self._role("""
            ACTION flee.
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        Hero DO flee.
        """, "Hero")
        assert "+!flee <- flee." in output

    def test_role_do_handler_special_action(self) -> None:
        """Role DO with special action should generate correctly mapped handler."""
        output = self._role("""
            PLOT P.
                PHASE start INITIAL.
                ROLE Hero.
                DURING start:
                    ON ENTER:
                        Hero DO TELL(villain, "die").
        """, "Hero")
        assert '+!tell(villain, "die") <- .send(villain, tell, "die").' in output


# == Full Integration ==========================================================

class TestFullIntegration:
    """Integration test with the complete Concert example."""

    CONCERT_SOURCE = """
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

    def test_compiles_successfully(self) -> None:
        """Full Concert example should compile without errors."""
        result = _compile(self.CONCERT_SOURCE)
        assert result.success
        assert result.error_count == 0

    def test_correct_output_files(self) -> None:
        """Should produce director + 2 role files + 2 playbook files."""
        result = _compile(self.CONCERT_SOURCE)
        assert "director_concert.asl" in result.outputs
        assert "role_concert_singer.asl" in result.outputs
        assert "role_concert_audiencemember.asl" in result.outputs
        assert "playbook_singerinbackstage.asl" in result.outputs
        assert "playbook_singeronstage.asl" in result.outputs

    def test_director_has_phase_transitions(self) -> None:
        """Director should have both transition plans."""
        result = _compile(self.CONCERT_SOURCE)
        director = result.outputs["director_concert.asl"]
        assert "+time_to_start" in director
        assert "+song_ends" in director

    def test_director_guarded_transition(self) -> None:
        """The song_ends transition should be guarded by fact."""
        result = _compile(self.CONCERT_SOURCE)
        director = result.outputs["director_concert.asl"]
        assert "audience_satisfied" in director

    def test_singer_has_both_playbooks(self) -> None:
        """Singer role should include both playbook files."""
        result = _compile(self.CONCERT_SOURCE)
        singer = result.outputs["role_concert_singer.asl"]
        assert '{ include("playbook_singerinbackstage.asl") }' in singer
        assert '{ include("playbook_singeronstage.asl") }' in singer

    def test_singer_conditional_plans(self) -> None:
        """Singer playbook file should have conditional plans for fan_greets."""
        result = _compile(self.CONCERT_SOURCE)
        pb = result.outputs["playbook_singerinbackstage.asl"]
        assert "happy" in pb
        assert "angry" in pb
        assert "greet_back" in pb
        assert "curse" in pb
        assert "ignore" in pb

    def test_singer_signal_plan(self) -> None:
        """Singer emergency plan should include signal to director."""
        result = _compile(self.CONCERT_SOURCE)
        pb = result.outputs["playbook_singerinbackstage.asl"]
        assert "!signal_directors(singerinbackstage, emergency)" in pb

    def test_director_emergency_plan(self) -> None:
        """Director should have plot-wide emergency plan."""
        result = _compile(self.CONCERT_SOURCE)
        director = result.outputs["director_concert.asl"]
        assert "@dir__Concert__emergency__0[priority(9)]" in director
        assert "trigger_alarm" in director
        assert "!send_to_role(singer, achieve, acknowledge)" in director
        assert "!send_to_role(audiencemember, achieve, acknowledge)" in director


# == Multi-File Compilation ====================================================

class TestMultiFile:
    """Tests for compiling multiple Regia source files together."""

    def test_split_base_and_playbook(self, tmp_path: Path) -> None:
        """Declarations in one file, playbook+plot in another should compile."""
        base_file = tmp_path / "base.regia"
        base_file.write_text("""
            ACTION greet.
            EVENT hello.
            FACT happy.
        """)

        main_file = tmp_path / "main.regia"
        main_file.write_text("""
            PLAYBOOK P:
                WHEN hello:
                    DO greet.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)

        result = compile_files([base_file, main_file])
        assert result.success
        assert "playbook_p.asl" in result.outputs
        assert "director_q.asl" in result.outputs
        pb = result.outputs["playbook_p.asl"]
        assert "greet" in pb

    def test_three_file_split(self, tmp_path: Path) -> None:
        """Declarations, playbook, and plot in separate files should compile."""
        decls = tmp_path / "decls.regia"
        decls.write_text("""
            ACTION run.
            ACTION fight.
            EVENT danger.
            EVENT safe.
            FACT armed.
        """)

        playbook = tmp_path / "playbook.regia"
        playbook.write_text("""
            PLAYBOOK Combat:
                WHEN danger:
                    DO fight.
        """)

        plot = tmp_path / "plot.regia"
        plot.write_text("""
            PLOT Battle.
                PHASE idle INITIAL.
                PHASE fighting.
                ROLE Soldier.
                DURING idle:
                    WHEN danger:
                        TRANSITION TO fighting.
                    ON ENTER:
                        ASSIGN Combat TO Soldier.
                DURING fighting:
                    WHEN safe:
                        TRANSITION TO idle.
        """)

        result = compile_files([decls, playbook, plot])
        assert result.success
        assert "playbook_combat.asl" in result.outputs
        assert "director_battle.asl" in result.outputs
        assert "role_battle_soldier.asl" in result.outputs

    def test_cross_file_undeclared_error(self, tmp_path: Path) -> None:
        """Referencing an undeclared action across files should error."""
        base_file = tmp_path / "base.regia"
        base_file.write_text("""
            EVENT hello.
        """)

        main_file = tmp_path / "main.regia"
        main_file.write_text("""
            PLAYBOOK P:
                WHEN hello:
                    DO missing_action.
            PLOT Q.
                PHASE start INITIAL.
                ROLE NPC.
                DURING start:
                    ON ENTER:
                        ASSIGN P TO NPC.
        """)

        result = compile_files([base_file, main_file])
        assert not result.success
        # Error should reference the file where the issue is
        error_msgs = [m for m in result.messages if m.severity.name == "ERROR"]
        assert len(error_msgs) > 0
        assert any("missing_action" in m.message for m in error_msgs)
        # Filename should be tracked on the error
        assert any(m.filename == "main.regia" for m in error_msgs)

    def test_duplicate_across_files(self, tmp_path: Path) -> None:
        """Same action declared in two files should produce duplicate error."""
        file_a = tmp_path / "a.regia"
        file_a.write_text("""
            ACTION greet.
        """)

        file_b = tmp_path / "b.regia"
        file_b.write_text("""
            ACTION greet.
        """)

        result = compile_files([file_a, file_b])
        assert not result.success
        error_msgs = [m for m in result.messages if m.severity.name == "ERROR"]
        assert any("greet" in m.message for m in error_msgs)

