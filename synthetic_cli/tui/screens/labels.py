"""Screen for defining labels."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Input, Static
from textual.containers import Grid

from .label_description import LabelDescriptionScreen

class LabelsScreen(Screen):
    """Screen for defining labels."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 2: Define Labels"),
            Static("Enter comma-separated labels (e.g., 'positive,negative')"),
            Input(placeholder="positive, negative, neutral", id="labels_input"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            labels_str = self.query_one("#labels_input", Input).value
            if labels_str:
                labels = [label.strip() for label in labels_str.split(',')]
                self.app.config.use_case_config.labels = labels
                self.app.push_screen(LabelDescriptionScreen())
