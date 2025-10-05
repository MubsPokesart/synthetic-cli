"""Screen for defining label descriptions."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, TextArea
from textual.containers import Grid

from .categories import CategoriesScreen

class LabelDescriptionScreen(Screen):
    """Screen for defining label descriptions."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 3: Describe Labels"),
            TextArea(id="label_description_input", language="markdown"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Create placeholder text
        labels = self.app.config.use_case_config.labels
        placeholder = "\n".join([f"{label}: [description]" for label in labels])
        self.query_one(TextArea).text = placeholder

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            self.app.config.use_case_config.label_descriptions = self.query_one(TextArea).text
            self.app.push_screen(CategoriesScreen())

