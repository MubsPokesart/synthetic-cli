"""
The main entrypoint for the CLI application, powered by Typer.

This module defines the main `app` and registers the `generate` command.
It handles the top-level command structure and help text.
"""

import typer
from rich.console import Console

from synthetic_cli.commands import generate

# Create a rich console for consistent output
console = Console()

# Initialize the Typer application
app = typer.Typer(
    name="synthetic-cli",
    help="A modern CLI for generating synthetic data.",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
)

# Add the 'generate' command to the main application.
app.command()(generate.run_generation_flow)

if __name__ == "__main__":
    app()