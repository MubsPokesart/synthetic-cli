"""Initial welcome screen for the application."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Static
from textual.containers import Grid

from .use_case import UseCaseScreen

class WelcomeScreen(Screen):
    """The initial welcome screen."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Welcome to the Synthetic Data Generation CLI!", id="title"),
            Static("This tool will guide you through a configuration of a synthetic data generation task.", id="subtitle"),
            Button("Start Configuration", variant="primary", id="start"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen(UseCaseScreen())
