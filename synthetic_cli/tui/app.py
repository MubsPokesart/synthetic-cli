import time

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import (
    Button, Header, Footer, Input, Label, RadioSet, Static, LoadingIndicator
)
from textual.worker import Worker, WorkerState

from synthetic_cli.config.models import GenerationConfig

class WelcomeScreen(Screen):
    """The initial welcome screen."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Welcome to the Synthetic Data Generation CLI!", id="title"),
            Static("This tool will guide you through configuring and running a synthetic data generation task.", id="subtitle"),
            Button("Start Configuration", variant="primary", id="start"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen(UseCaseScreen())

class UseCaseScreen(Screen):
    """Screen for selecting the use case."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 1: Select a Use Case"),
            RadioSet(*self.app.config.available_use_cases, id="use_case_select"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            use_case_select = self.query_one(RadioSet)
            if use_case_select.pressed_button:
                self.app.config.use_case = use_case_select.pressed_button.label
                self.app.push_screen(LabelsScreen())

class GenerationScreen(Screen):
    """Shows a loading indicator while data is being generated."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            LoadingIndicator(),
            Static("Starting...", id="status"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.run_generation_worker()

    def run_generation_worker(self) -> None:
        self.run_worker(self.generation_worker, thread=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            grid = self.query_one(Grid)
            grid.remove_children()
            grid.mount(
                Label("✔ Data generation complete!", id="title"),
                Button("Exit", variant="primary", id="exit"),
            )

    def generation_worker(self) -> None:
        """Simulates a long-running data generation task."""
        status = self.query_one("#status", Static)
        for i in range(101):
            status.update(f"Progress: {i}%")
            time.sleep(0.05)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()

class SummaryScreen(Screen):
    """Displays a summary of the configuration and asks for confirmation."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Configuration Summary", id="title"),
            Static(self.get_summary_text(), id="summary"),
            Button("Generate", variant="primary", id="generate"),
            Button("Back", id="back"),
            id="dialog",
        )
        yield Footer()

    def get_summary_text(self) -> str:
        config = self.app.config
        return (
            f"[bold]Use Case:[/bold] {config.use_case}\n"
            f"[bold]Labels:[/bold] {', '.join(config.labels)}\n"
            f"[bold]Model:[/bold] {config.model}\n"
            f"[bold]API Key:[/bold] {'*' * 12}\n"
            f"[bold]Output Path:[/bold] {config.output_path}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "generate":
            self.app.push_screen(GenerationScreen())

class ModelSelectionScreen(Screen):
    """Screen for selecting the generation model."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Label("Step 3: Select a Model"),
            RadioSet(*self.app.config.available_models, id="model_select"),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            model_select = self.query_one(RadioSet)
            if model_select.pressed_button:
                self.app.config.model = model_select.pressed_button.label
                self.app.push_screen(APIKeyScreen())

class LabelsScreen(Screen):
    # ... (This class is unchanged)
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
                self.app.push_screen(ModelSelectionScreen())

class APIKeyScreen(Screen):
    """Screen for entering the API key."""
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
                self.app.push_screen(SummaryScreen())


class ConfiguratorApp(App):
    CSS_PATH = "app.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.config = GenerationConfig()

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark