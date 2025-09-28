"""
The Textual-based full-screen interactive configuration editor.

This TUI guides the user through the configuration steps in a polished,
full-screen interface, ensuring a valid configuration is created before
proceeding.
"""

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Button, Header, Footer, Input, Label, RadioButtons, Static
)

from synthetic_cli.config.models import GenerationConfig

class WelcomeScreen(Screen):
    """The initial screen to welcome the user."""
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Welcome to the Synthetic Data Generator", id="title"),
            Static(
                "This tool will guide you through configuring a new "
                "data generation task.",
                id="subtitle",
            ),
            Button("Start Configuration", variant="primary", id="start"),
            Button("Quit", id="quit"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen(UseCaseScreen())
        elif event.button.id == "quit":
            self.app.exit(None)

class UseCaseScreen(Screen):
    """Screen for selecting the generation use case."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 1: Select a Use Case"),
            RadioButtons(
                "Text Classification",
                "Text Summarization",
                "Question Answering",
                id="use_case",
            ),
            Button("Next", variant="primary", id="next"),
            id="dialog"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            radio_buttons = self.query_one(RadioButtons)
            if radio_buttons.pressed_button:
                self.app.config.use_case = radio_buttons.pressed_button.label
                self.app.push_screen(LabelsScreen())

class LabelsScreen(Screen):
    """Screen for defining data labels."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 2: Define Labels"),
            Static("Enter comma-separated labels (e.g., 'positive,negative')"),
            Input(placeholder="positive, negative, neutral", id="labels_input"),
            Button("Next", variant="primary", id="next"),
            id="dialog"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            labels_str = self.query_one("#labels_input", Input).value
            if labels_str:
                labels = [label.strip() for label in labels_str.split(',')]
                self.app.config.labels = labels
                self.app.push_screen(APIKeyScreen())

class APIKeyScreen(Screen):
    """Screen for entering the API Key."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 3: Enter your API Key"),
            Input(placeholder="sk-...", password=True, id="api_key_input"),
            Button("Finish Configuration", variant="primary", id="finish"),
            id="dialog"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "finish":
            key = self.query_one("#api_key_input", Input).value
            if key:
                self.app.config.api_key = key
                self.app.exit(self.app.config)

class ConfiguratorApp(App):
    """A Textual app to configure data generation."""

    CSS_PATH = None  # No external CSS for this minimal example
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.config = GenerationConfig()

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark