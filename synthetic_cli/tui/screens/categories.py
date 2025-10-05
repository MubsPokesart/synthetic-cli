"""Screen for defining categories and types."""

import json
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, TextArea, Static
from textual.containers import Grid

from .examples import ExamplesScreen

class CategoriesScreen(Screen):
    """Screen for defining categories and their types."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 4: Define Categories and Types"),
            Static("Enter a JSON object mapping category names to a list of types."),
            TextArea(id="categories_input", language="json"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Placeholder content
        placeholder = {
            "customer_service": ["complaint", "inquiry", "compliment"],
            "sales": ["pre-sale question", "post-sale support"]
        }
        self.query_one(TextArea).text = json.dumps(placeholder, indent=4)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            try:
                categories_text = self.query_one(TextArea).text
                self.app.config.use_case_config.categories_types = json.loads(categories_text)
                self.app.push_screen(ExamplesScreen())
            except json.JSONDecodeError:
                self.app.bell()
                # TODO: Add a proper error message to the user
