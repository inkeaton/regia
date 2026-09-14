"""
Command-line interface for the Regia compiler.

Exposes two public commands:
    regia compile <file.regia> [-o <output_dir>] [--dry-run]
    regia check   <file.regia>

Hidden debug command:
    regia dump-ast <file.regia>  (pretty-prints the validated AST)
"""

import sys
from dataclasses import dataclass
from pathlib     import Path
from pprint      import pprint

import click

from regia          import __version__
from regia.compiler import compile_file
from regia.errors   import format_message, Severity


# == Shared state ==============================================================

@dataclass
class CliState:
    """Shared state passed between CLI commands via the Click context.

    Attributes:
        quiet: Suppress all output except errors.
    """
    quiet: bool = False


# == CLI entry point ===========================================================

@click.group()
@click.version_option(version=__version__)
@click.option("--quiet", is_flag=True, help="Only print errors, suppress normal output.")
@click.pass_context
def main(ctx: click.Context, quiet: bool) -> None:
    """Regia Compiler CLI."""
    ctx.obj = CliState(quiet=quiet)


# == Output helpers ============================================================

def _print_diagnostics(result, quiet: bool) -> None:
    """Print all diagnostics from a CompileResult, sorted by file and line.

    Args:
        result: The CompileResult containing messages.
        quiet:  If True, suppress warnings and only print errors.
    """
    for msg in sorted(result.messages, key=lambda m: (m.filename, m.line)):
        if quiet and msg.severity != Severity.ERROR:
            continue
        click.echo(format_message(msg, click.style))


def _print_summary(result, quiet: bool, action_name: str = "Compilation") -> None:
    """Print the final success or failure summary line and exit on failure.

    Args:
        result:      The CompileResult to summarise.
        quiet:       If True, suppress the success message.
        action_name: The verb to use in the summary (e.g. 'Compilation', 'Check').
    """
    if not result.success:
        click.secho(
            f"\n{action_name} failed with {result.error_count} error(s).",
            fg="red",
            bold=True,
        )
        sys.exit(1)

    if not quiet:
        click.secho(
            f"\n{action_name} successful! ({result.warning_count} warning(s))",
            fg="green",
            bold=True,
        )


# == Commands ==================================================================

@main.command()
@click.argument(
    "source_file", required=True,
    type=click.Path(exists=True, path_type=Path),
)

@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    default=".",
    help="Directory to place the generated AgentSpeak files (defaults to CWD).",
)

@click.option(
    "--dry-run",
    is_flag=True,
    help="Run the full pipeline but do not write any files to disk.",
)

@click.pass_context
def compile(ctx: click.Context, source_file: Path, output_dir: Path, dry_run: bool) -> None:
    """Compile a Regia source file into AgentSpeak."""
    state: CliState = ctx.obj

    if not state.quiet:
        click.echo(f"Compiling {source_file.name}...")

    result = compile_file(source_file)

    _print_diagnostics(result, state.quiet)
    _print_summary(result, state.quiet)

    # Write output files to disk
    if not result.outputs:
        if not state.quiet:
            click.echo("No output files generated (source was empty or had no plots).")
        return

    # In dry-run mode, always show the file listing so the user gets feedback
    # even when --quiet is active.
    show_files = dry_run or not state.quiet

    if show_files:
        if dry_run:
            click.echo(f"\nWould write AgentSpeak files to {output_dir.resolve()}/ (dry-run)")
        else:
            click.echo(f"\nWriting AgentSpeak files to {output_dir.resolve()}/")

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in result.outputs.items():
        if not dry_run:
            out_path = output_dir / filename
            out_path.write_text(content, encoding="utf-8")
        if show_files:
            click.echo(f"  - {filename}")


@main.command()
@click.argument(
    "source_file", required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.pass_context
def check(ctx: click.Context, source_file: Path) -> None:
    """Validate a Regia source file without emitting code."""
    state: CliState = ctx.obj

    if not state.quiet:
        click.echo(f"Checking {source_file.name}...")

    result = compile_file(source_file, emit=False)

    _print_diagnostics(result, state.quiet)
    _print_summary(result, state.quiet, action_name="Check")


@main.command(name="dump-ast", hidden=True)
@click.argument(
    "source_file", required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.pass_context
def dump_ast(ctx: click.Context, source_file: Path) -> None:
    """Run the full pipeline (without emission) and pretty-print the AST.

    This command is intended for internal compiler debugging only.
    IMPORT statements are fully resolved and validation is run
    before the AST is dumped.
    """
    # Run Stages 0-4 (with import resolution) but skip emission
    result = compile_file(source_file, emit=False)

    if result.ast:
        pprint(result.ast)

    if not result.success:
        click.secho(
            f"\nAST dump failed with {result.error_count} error(s).",
            fg="red", bold=True,
        )
        sys.exit(1)


# == Entry point ===============================================================

if __name__ == "__main__":
    main()
