"""
Contains the core logic for the 'generate' command.
"""

from typing import Optional
from rich.console import Console
from synthetic_cli.config.models import GenerationConfig
from synthetic_cli.tui.app import ConfiguratorApp

console = Console()

def generate_data(config: GenerationConfig):
    """Generates data based on the given config."""
    console.print("Generating data with the following configuration:")
    console.print(config)

def run_generation_flow(config: Optional[GenerationConfig] = None):
    """Launches the Textual TUI application or generates data directly."""
    if config:
        generate_data(config)
    else:
        app = ConfiguratorApp()
        app.run()