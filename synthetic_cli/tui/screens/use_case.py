"""Screen for selecting the use case."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, RadioSet, RadioButton
from textual.containers import Grid

from .labels import LabelsScreen

class UseCaseScreen(Screen):
    """Screen for selecting the use case."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 1: Select a Use Case"),
            RadioSet("text classification", "data generation", "summarization", id="use_case_select"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Set default value
        self.query_one(RadioSet).query(RadioButton).first().value = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            use_case_select = self.query_one(RadioSet)
            if use_case_select.pressed_button:
                self.app.config.use_case_config.use_case = str(use_case_select.pressed_button.label)
                self.app.push_screen(LabelsScreen())
