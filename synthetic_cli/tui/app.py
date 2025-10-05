"""
Main Textual application for the Synthetic Data Generation CLI.
"""

from textual.app import App

from synthetic_cli.config.models import GenerationConfig
from .screens import WelcomeScreen

class ConfiguratorApp(App):
    """The main application class for the TUI."""

    CSS_PATH = "app.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.config = GenerationConfig()

    def on_mount(self) -> None:
        """Pushes the welcome screen when the app is mounted."""
        self.push_screen(WelcomeScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
