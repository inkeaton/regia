"""
Command-line interface for the Regia compiler.

Usage:
    regia compile <file.regia> [<file2.regia> ...] [-o <output_dir>]
    regia check <file.regia> [<file2.regia> ...]
    regia parse <file.regia> [<file2.regia> ...]
"""

import sys
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Tuple

import click

from regia import __version__
from regia.compiler import compile_file, compile_files, parse_files
from regia.errors import Severity


@dataclass
class CliState:
    """Shared state for CLI commands."""
    quiet: bool = False
    verbose: bool = False


@click.group()
@click.version_option(version=__version__)
@click.option("--quiet", is_flag=True, help="Only print errors, suppress normal output.")
@click.option("--verbose", is_flag=True, help="Print detailed stage progression.")
@click.pass_context
def main(ctx: click.Context, quiet: bool, verbose: bool) -> None:
    """Regia Compiler CLI."""
    ctx.obj = CliState(quiet=quiet, verbose=verbose)


def _print_diagnostics(result, quiet: bool) -> None:
    """Helper to print diagnostics consistently."""
    for msg in result.messages:
        # If quiet, only print errors
        if quiet and msg.severity != Severity.ERROR:
            continue

        prefix = f"[{msg.severity.name}]"
        if msg.severity == Severity.ERROR:
            prefix = click.style(prefix, fg="red", bold=True)
        elif msg.severity == Severity.WARNING:
            prefix = click.style(prefix, fg="yellow", bold=True)

        # Include filename in location when available
        if msg.filename:
            colored_name = click.style(msg.filename, fg="blue")
            location = f"{colored_name}:{msg.line}, col {msg.column}"
        else:
            location = f"line {msg.line}, col {msg.column}"

        click.echo(f"{prefix} {location}: {msg.message}")


def _print_summary(result, quiet: bool) -> None:
    """Helper to print compilation summary consistently."""
    if not result.success:
        click.secho(
            f"\nCompilation failed with {result.error_count} error(s).",
            fg="red",
            bold=True,
        )
        sys.exit(1)

    if not quiet:
        click.secho(
            f"\nCompilation successful! ({result.warning_count} warning(s))",
            fg="green",
            bold=True,
        )


@main.command()
@click.argument(
    "source_files", nargs=-1, required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    default=".",
    help="Directory to place the generated AgentSpeak files.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run the full pipeline but do not write any files to disk.",
)
@click.pass_context
def compile(ctx: click.Context, source_files: Tuple[Path, ...], output_dir: Path, dry_run: bool) -> None:
    """Compile one or more Regia source files into AgentSpeak."""
    state: CliState = ctx.obj
    file_list = list(source_files)
    file_names = ", ".join(f.name for f in file_list)

    if not state.quiet:
        click.echo(f"Compiling {file_names}...")

    # Run the compiler pipeline
    if len(file_list) == 1:
        if state.verbose:
            click.echo("Running single-file compilation pipeline...")
        result = compile_file(file_list[0])
    else:
        if state.verbose:
            click.echo(f"Running multi-file compilation pipeline for {len(file_list)} files...")
        result = compile_files(file_list)

    _print_diagnostics(result, state.quiet)
    _print_summary(result, state.quiet)

    # Write output files
    if not result.outputs:
        if not state.quiet:
            click.echo("No output files generated (source was empty or had no plots).")
        return

    if not state.quiet:
        if dry_run:
            click.echo(f"\nWould write AgentSpeak files to {output_dir.resolve()}/ (dry-run)")
        else:
            click.echo(f"\nWriting AgentSpeak files to {output_dir.resolve()}/")
            output_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in result.outputs.items():
        if not dry_run:
            out_path = output_dir / filename
            out_path.write_text(content, encoding="utf-8")
        if not state.quiet:
            click.echo(f"  - {filename}")


@main.command()
@click.argument(
    "source_files", nargs=-1, required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.pass_context
def check(ctx: click.Context, source_files: Tuple[Path, ...]) -> None:
    """Parse and validate files without emitting code."""
    state: CliState = ctx.obj
    file_list = list(source_files)
    file_names = ", ".join(f.name for f in file_list)

    if not state.quiet:
        click.echo(f"Checking {file_names}...")

    if len(file_list) == 1:
        if state.verbose:
            click.echo("Running single-file validation...")
        result = compile_file(file_list[0], emit=False)
    else:
        if state.verbose:
            click.echo(f"Running multi-file validation for {len(file_list)} files...")
        result = compile_files(file_list, emit=False)

    _print_diagnostics(result, state.quiet)
    
    if not result.success:
        click.secho(
            f"\nCheck failed with {result.error_count} error(s).",
            fg="red",
            bold=True,
        )
        sys.exit(1)
        
    if not state.quiet:
        click.secho(
            f"\nCheck passed! ({result.warning_count} warning(s))",
            fg="green",
            bold=True,
        )


@main.command()
@click.argument(
    "source_files", nargs=-1, required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.pass_context
def parse(ctx: click.Context, source_files: Tuple[Path, ...]) -> None:
    """Parse source files and print the generated AST."""
    state: CliState = ctx.obj
    file_list = list(source_files)
    
    if state.verbose:
        click.echo(f"Parsing {len(file_list)} file(s)...")
        
    program = parse_files(file_list)
    pprint(program)


if __name__ == "__main__":
    main()
