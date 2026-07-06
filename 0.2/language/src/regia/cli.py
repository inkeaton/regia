"""
Command-line interface for the Regia compiler.

Usage:
    regia compile <file.regia> [<file2.regia> ...] [-o <output_dir>]
"""

import sys
from pathlib import Path
from typing import Tuple

import click

from regia.compiler import compile_file, compile_files
from regia.errors import Severity


@click.group()
def main() -> None:
    """Regia Compiler CLI."""
    pass


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
def compile(source_files: Tuple[Path, ...], output_dir: Path) -> None:
    """Compile one or more Regia source files into AgentSpeak."""
    file_list = list(source_files)
    file_names = ", ".join(f.name for f in file_list)
    click.echo(f"Compiling {file_names}...")

    # Run the compiler pipeline
    if len(file_list) == 1:
        result = compile_file(file_list[0])
    else:
        result = compile_files(file_list)

    # Print diagnostics
    for msg in result.messages:
        # Format based on severity
        prefix = f"[{msg.severity.name}]"
        if msg.severity == Severity.ERROR:
            prefix = click.style(prefix, fg="red", bold=True)
        elif msg.severity == Severity.WARNING:
            prefix = click.style(prefix, fg="yellow", bold=True)

        # Include filename in location when available
        if msg.filename:
            location = f"{msg.filename}:{msg.line}, col {msg.column}"
        else:
            location = f"line {msg.line}, col {msg.column}"

        click.echo(f"{prefix} {location}: {msg.message}")

    # Summary
    if not result.success:
        click.secho(
            f"\nCompilation failed with {result.error_count} error(s).",
            fg="red",
            bold=True,
        )
        sys.exit(1)

    click.secho(
        f"\nCompilation successful! ({result.warning_count} warning(s))",
        fg="green",
        bold=True,
    )

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write output files
    if not result.outputs:
        click.echo("No output files generated (source was empty or had no plots).")
        return

    click.echo(f"\nWriting AgentSpeak files to {output_dir.resolve()}/")
    for filename, content in result.outputs.items():
        out_path = output_dir / filename
        out_path.write_text(content, encoding="utf-8")
        click.echo(f"  - {filename}")


if __name__ == "__main__":
    main()
