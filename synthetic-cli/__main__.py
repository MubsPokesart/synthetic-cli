
"""
Allows the package to be run as a script via `python -m synthetic_cli`.
This provides a consistent entrypoint for the command-line interface.
"""

from synthetic_cli.cli import app

if __name__ == "__main__":
    app()