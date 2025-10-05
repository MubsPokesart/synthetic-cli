"""Screen for providing prompt examples."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, TextArea, Static
from textual.containers import Grid

from .model_selection import ModelSelectionScreen

class ExamplesScreen(Screen):
    """Screen for providing few-shot examples."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 5: Provide Prompt Examples"),
            Static("Provide examples for the model to follow."),
            TextArea(id="examples_input", language="markdown"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Placeholder content
        placeholder = """
LABEL: positive
CATEGORY: customer_service
TYPE: compliment
OUTPUT: Thank you so much for the excellent service!
REASONING: This expresses gratitude and praise, indicating positive sentiment.

LABEL: negative
CATEGORY: customer_service
TYPE: complaint
OUTPUT: I am very disappointed with the product quality.
REASONING: This expresses disappointment, indicating negative sentiment.
"""
        self.query_one(TextArea).text = placeholder

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            self.app.config.use_case_config.prompt_examples = self.query_one(TextArea).text
            self.app.push_screen(ModelSelectionScreen())
