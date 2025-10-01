"""
The main entrypoint for the CLI application, powered by Typer.
"""

import typer
from synthetic_cli.commands import generate as generate_command

app = typer.Typer(no_args_is_help=False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        generate_command.run_generation_flow()

if __name__ == "__main__":
    app()
