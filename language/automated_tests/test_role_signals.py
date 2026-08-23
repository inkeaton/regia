import pytest
from textwrap import dedent

from regia.compiler import compile_source


def test_when_role_signals_success():
    """Test successful compilation of WHEN ROLE SIGNALS."""
    source = dedent("""
        EVENT done.
        EVENT warning.
        
        PLOT Main.
            PHASE start INITIAL.
            PHASE next_phase.
            ROLE Hero.
            
            DURING start:
                WHEN ROLE Hero SIGNALS done:
                    TRANSITION TO next_phase.
                    
                WHEN ROLE Hero SIGNALS warning PRIORITY 5:
                    WORLD DO PRINT("warning").
    """)
    result = compile_source(source)
    assert result.success, "Compilation failed: " + str(result.messages)
    
    assert "director_main.asl" in result.outputs
    asl = result.outputs["director_main.asl"]
    
    # Assert exactly one + before event, not two (guard against ++ regression)
    assert "\n+done[source(Sender)] : current_phase(start) & role_agent(hero, Sender) <-" in asl
    assert "\n+warning[source(Sender)] : current_phase(start) & role_agent(hero, Sender) <-" in asl
    assert "++" not in asl  # regression guard
    assert "@dir__Main__hero_signals_warning__0[priority(5)]" in asl


def test_when_role_signals_branches():
    """Test IF/ELSE branches in WHEN ROLE SIGNALS."""
    source = dedent("""
        FACT injured.
        EVENT ping.
        
        PLOT Main.
            PHASE start INITIAL.
            ROLE Hero.
            
            DURING start:
                WHEN ROLE Hero SIGNALS ping:
                    IF injured:
                        WORLD DO PRINT("Ouch").
                    ELSE:
                        WORLD DO PRINT("All good").
    """)
    result = compile_source(source)
    assert result.success, "Compilation failed: " + str(result.messages)
    
    asl = result.outputs["director_main.asl"]
    
    # Check IF branch — exactly one leading +
    assert "\n+ping[source(Sender)] : current_phase(start) & role_agent(hero, Sender) & injured <-" in asl
    # Check ELSE branch
    assert "\n+ping[source(Sender)] : current_phase(start) & role_agent(hero, Sender) & not (injured) <-" in asl
    assert "++" not in asl  # regression guard


def test_when_role_signals_unknown_role():
    """Test validation error for unknown role."""
    source = dedent("""
        EVENT done.
        
        PLOT Main.
            PHASE start INITIAL.
            ROLE Hero.
            
            DURING start:
                WHEN ROLE Villain SIGNALS done:
                    WORLD DO PRINT("done").
    """)
    result = compile_source(source)
    assert not result.success
    assert any("references undeclared role: 'Villain'" in msg.message for msg in result.messages)


def test_when_role_signals_unknown_event():
    """Test validation error for unknown event."""
    source = dedent("""
        PLOT Main.
            PHASE start INITIAL.
            ROLE Hero.
            
            DURING start:
                WHEN ROLE Hero SIGNALS nope:
                    WORLD DO PRINT("nope").
    """)
    result = compile_source(source)
    assert not result.success
    assert any("Undeclared event: 'nope'." in msg.message for msg in result.messages)
