"""Screen for configuring output settings."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Input, Checkbox, Static
from textual.containers import Grid, Horizontal

from .summary import SummaryScreen

class OutputSettingsScreen(Screen):
    """Screen for configuring output settings."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 8: Output Settings"),
            Horizontal(Static("Sample Size: ", classes="label"), Input(value="100", id="sample_size", classes="input"),),
            Horizontal(Static("Batch Size: ", classes="label"), Input(value="20", id="batch_size", classes="input"),),
            Horizontal(Static("Output Directory: ", classes="label"), Input(value="./generated_data", id="output_dir", classes="input"),),
            Checkbox("Save Reasoning", value=True, id="save_reasoning"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            self.app.config.output_config.sample_size = int(self.query_one("#sample_size", Input).value)
            self.app.config.output_config.batch_size = int(self.query_one("#batch_size", Input).value)
            self.app.config.output_config.output_dir = self.query_one("#output_dir", Input).value
            self.app.config.output_config.save_reasoning = self.query_one("#save_reasoning", Checkbox).value
            self.app.push_screen(SummaryScreen())
