"""
The main entrypoint for the CLI application, powered by Typer.
"""

import typer
from synthetic_cli.tui.app import ConfiguratorApp

app = typer.Typer(no_args_is_help=False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """The main entry point for the CLI application."""
    if ctx.invoked_subcommand is None:
        app = ConfiguratorApp()
        app.run()

if __name__ == "__main__":
    app()
