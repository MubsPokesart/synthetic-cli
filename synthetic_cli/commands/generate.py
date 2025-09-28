"""
Contains the core logic for the 'generate' command.
"""

import sys
import time
from typing import List, Optional

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

# Corrected import paths
from synthetic_cli.config.models import GenerationConfig
from synthetic_cli.tui.app import ConfiguratorApp

console = Console()

def display_summary(config: GenerationConfig):
    # ... (function content remains the same)
    summary = Text(justify="left")
    summary.append("Configuration Summary\n", style="bold magenta")
    summary.append("-----------------------\n")
    summary.append(f"Use Case: {config.use_case}\n", style="cyan")
    summary.append(f"Labels: {', '.join(config.labels)}\n", style="cyan")
    summary.append(f"Model: {config.model}\n", style="cyan")
    summary.append(f"API Key: {'*' * 12}\n", style="cyan")
    summary.append(f"Output Path: {config.output_path}\n", style="cyan")
    console.print(Panel(summary, title="Ready to Generate", border_style="green"))


def run_generation_process():
    # ... (function content remains the same)
    with console.status("[bold green]Generating synthetic data...") as status:
        status.spinner = "dots"
        time.sleep(1)
        status.update("Connecting to generation service...")
        time.sleep(2)
        status.update("Submitting generation task...")
        time.sleep(2)
        status.update("Waiting for results...")
        time.sleep(3)
    console.print("[bold green]✔ Data generation complete![/bold green]")


def run_generation_flow(
    use_case: Optional[str] = typer.Option(
        None, "--use-case", "-u", help="The data generation use case."
    ),
    labels: Optional[List[str]] = typer.Option(
        None, "--label", "-l", help="A label for data generation (can be used multiple times)."
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", help="API key for the generation service.", envvar="SYNTH_API_KEY"
    ),
    output_path: str = typer.Option(
        "./synthetic_data.csv", "--output", "-o", help="Path to save the output file."
    ),
):
    # ... (function content remains the same)
    config = GenerationConfig()
    is_interactive_flow = not (use_case and labels and api_key)

    if is_interactive_flow:
        app = ConfiguratorApp()
        returned_config = app.run()
        if returned_config is None:
            console.print("[bold red]Configuration cancelled. Exiting.[/bold red]")
            sys.exit(1)
        config = returned_config
    else:
        config.use_case = use_case
        config.labels = labels
        config.api_key = api_key
        config.output_path = output_path

    display_summary(config)
    try:
        proceed = questionary.confirm(
            "Proceed with data generation?", default=True
        ).ask()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red]Operation cancelled by user.[/bold red]")
        sys.exit(1)

    if not proceed:
        console.print("[bold yellow]Generation cancelled by user.[/bold yellow]")
        sys.exit(0)

    run_generation_process()
    sys.exit(0)