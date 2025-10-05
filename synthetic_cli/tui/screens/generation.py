"""Screen that shows the data generation progress."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Static, LoadingIndicator
from textual.containers import Grid
from textual.worker import Worker, WorkerState

from synthetic_cli.commands.generate import generate_data

class GenerationScreen(Screen):
    """Shows a loading indicator while data is being generated."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            LoadingIndicator(),
            Static("Starting data generation...", id="status"),
            id="dialog",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Starts the generation worker when the screen is mounted."""
        self.run_generation_worker()

    def run_generation_worker(self) -> None:
        """Runs the data generation in a separate thread."""
        self.run_worker(self.generation_worker, thread=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handles worker state changes."""
        if event.state == WorkerState.SUCCESS:
            grid = self.query_one(Grid)
            grid.remove_children()
            grid.mount(
                Label("✔ Data generation complete!", id="title"),
                Button("Exit", variant="primary", id="exit"),
            )

    def generation_worker(self) -> None:
        """The actual worker function that calls the data generator."""
        generate_data(self.app.config)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()
