"""Screen for selecting the generation model."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, RadioSet
from textual.containers import Grid

from .token import TokenScreen

class ModelSelectionScreen(Screen):
    """Screen for selecting the generation model."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 6: Select a Model"),
            RadioSet(
                "meta-llama/Llama-3.2-3B-Instruct",
                "google/gemma-3-1b-it",
                "HuggingFaceTB/SmolLM2-1.7B-Instruct",
                id="model_select",
            ),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        # Set default value
        self.query_one(RadioSet).pressed_button = self.query_one(RadioSet).buttons[0]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            model_select = self.query_one(RadioSet)
            if model_select.pressed_button:
                self.app.config.model_config.model = str(model_select.pressed_button.label)
                self.app.push_screen(TokenScreen())
