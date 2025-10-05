"""Screen for entering the Hugging Face token."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Input
from textual.containers import Grid

from .output_settings import OutputSettingsScreen

class TokenScreen(Screen):
    """Screen for entering the Hugging Face token."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 7: Enter your Hugging Face Token"),
            Input(placeholder="hf_...", password=True, id="token_input"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            token = self.query_one("#token_input", Input).value
            if token:
                self.app.config.model_config.hf_token = token
                self.app.push_screen(OutputSettingsScreen())
