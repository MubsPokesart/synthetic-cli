"""Screen for displaying the configuration summary."""

import json
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Static
from textual.containers import Grid, Horizontal

from .generation import GenerationScreen

class SummaryScreen(Screen):
    """Displays a summary of the configuration and asks for confirmation."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Configuration Summary", id="title"),
            Static(self.get_summary_text(), id="summary"),
            Horizontal(
                Button("Generate", variant="primary", id="generate"),
                Button("Back", id="back"),
            ),
            id="dialog",
        )
        yield Footer()

    def get_summary_text(self) -> str:
        """Generates the summary text from the configuration."""
        config = self.app.config
        use_case = config.use_case_config
        model = config.model_config
        output = config.output_config

        # Pretty print the categories dictionary
        categories_str = json.dumps(use_case.categories_types, indent=4)

        return (
            f"[bold]Use Case:[/bold] {use_case.use_case}\n"
            f"[bold]Labels:[/bold] {', '.join(use_case.labels)}\n"
            f"[bold]Label Descriptions:[/bold]\n{use_case.label_descriptions}\n"
            f"[bold]Categories & Types:[/bold]\n{categories_str}\n"
            f"[bold]Prompt Examples:[/bold]\n{use_case.prompt_examples}\n\n"
            f"[bold]Model:[/bold] {model.model}\n"
            f"[bold]Max New Tokens:[/bold] {model.max_new_tokens}\n"
            f"[bold]HF Token:[/bold] {'********' if model.hf_token else 'Not Set'}\n\n"
            f"[bold]Sample Size:[/bold] {output.sample_size}\n"
            f"[bold]Batch Size:[/bold] {output.batch_size}\n"
            f"[bold]Output Directory:[/bold] {output.output_dir}\n"
            f"[bold]Save Reasoning:[/bold] {output.save_reasoning}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "generate":
            self.app.push_screen(GenerationScreen())
