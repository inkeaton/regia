"""
Command-line interface for the Regia compiler.

Usage:
    regia compile <file.regia> [-o <output_dir>]
"""

import sys
from pathlib import Path

import click

from regia.compiler import compile_file
from regia.errors import Severity


@click.group()
def main() -> None:
    """Regia Compiler CLI."""
    pass


@main.command()
@click.argument("source_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    default=".",
    help="Directory to place the generated AgentSpeak files.",
)
def compile(source_file: Path, output_dir: Path) -> None:
    """Compile a Regia source file into AgentSpeak."""
    click.echo(f"Compiling {source_file.name}...")

    # Run the compiler pipeline
    result = compile_file(source_file)

    # Print diagnostics
    for msg in result.messages:
        # Format based on severity
        prefix = f"[{msg.severity.name}]"
        if msg.severity == Severity.ERROR:
            prefix = click.style(prefix, fg="red", bold=True)
        elif msg.severity == Severity.WARNING:
            prefix = click.style(prefix, fg="yellow", bold=True)
            
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
