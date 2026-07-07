"""
Tests for the Regia compiler CLI.

Run with: pytest tests/test_cli.py -v
"""

from pathlib import Path
from click.testing import CliRunner

from regia.cli import main
from regia import __version__


def test_version() -> None:
    """Test that --version returns the correct version string."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output
    assert "version" in result.output


def test_check_command(tmp_path: Path) -> None:
    """Test the check command runs validation but doesn't emit."""
    source_file = tmp_path / "valid.regia"
    source_file.write_text("""
        ACTION run.
        PLOT Test.
            PHASE one INITIAL.
            ROLE Actor.
            DURING one:
                ON ENTER:
                    Actor DO run.
    """)

    runner = CliRunner()
    result = runner.invoke(main, ["check", str(source_file)])
    
    assert result.exit_code == 0
    assert "Checking valid.regia..." in result.output
    assert "Check passed!" in result.output
    
    # Ensure no files were written to the current dir or tmp_path
    asl_files = list(tmp_path.glob("*.asl"))
    assert len(asl_files) == 0


def test_check_command_fails_on_error(tmp_path: Path) -> None:
    """Test the check command exits with 1 on validation error."""
    source_file = tmp_path / "invalid.regia"
    source_file.write_text("""
        PLOT Test.
            PHASE one INITIAL.
            ROLE Actor.
            DURING one:
                ON ENTER:
                    Actor DO undeclared_action.
    """)

    runner = CliRunner()
    result = runner.invoke(main, ["check", str(source_file)])
    
    assert result.exit_code == 1
    assert "Check failed with 1 error(s)." in result.output
    assert "undeclared_action" in result.output


def test_parse_command(tmp_path: Path) -> None:
    """Test the parse command prints the AST."""
    source_file = tmp_path / "simple.regia"
    source_file.write_text("ACTION jump.")

    runner = CliRunner()
    result = runner.invoke(main, ["parse", str(source_file)])
    
    assert result.exit_code == 0
    # Check that pprint of the AST includes 'Program' and 'ActionDecl'
    assert "Program(" in result.output
    assert "ActionDecl(" in result.output
    assert "'jump'" in result.output


def test_compile_dry_run(tmp_path: Path) -> None:
    """Test compile --dry-run doesn't write files."""
    source_file = tmp_path / "test.regia"
    source_file.write_text("""
        ACTION run.
        PLOT Test.
            PHASE one INITIAL.
            ROLE Actor.
            DURING one:
                ON ENTER:
                    Actor DO run.
    """)

    out_dir = tmp_path / "output"
    
    runner = CliRunner()
    result = runner.invoke(main, ["compile", "--dry-run", "-o", str(out_dir), str(source_file)])
    
    assert result.exit_code == 0
    assert "Would write AgentSpeak files" in result.output
    assert "(dry-run)" in result.output
    assert "director_test.asl" in result.output
    
    # Ensure directory was not created or is empty
    if out_dir.exists():
        assert len(list(out_dir.glob("*.asl"))) == 0


def test_quiet_flag(tmp_path: Path) -> None:
    """Test --quiet suppresses non-error output."""
    source_file = tmp_path / "test.regia"
    # Create a valid program that also triggers a warning
    source_file.write_text("""
        ACTION unused_action.
        ACTION run.
        PLOT Test.
            PHASE one INITIAL.
            ROLE Actor.
            DURING one:
                ON ENTER:
                    Actor DO run.
    """)

    runner = CliRunner()
    result = runner.invoke(main, ["--quiet", "check", str(source_file)])
    
    assert result.exit_code == 0
    assert "Checking" not in result.output
    assert "Check passed!" not in result.output
    assert "warning(s)" not in result.output
    # The output should be completely empty since there are no errors (only a warning)
    assert result.output.strip() == ""
