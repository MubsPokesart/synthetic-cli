# Synthetic Data Generation CLI

A minimal, production-grade command-line tool for interactively configuring and running synthetic data generation tasks. This tool is built with a human-first design philosophy, prioritizing an intuitive and robust user experience.

\![Demo of the interactive TUI in action]

## Features

  * **Interactive TUI Mode**: A full-screen terminal interface, powered by Textual, guides you step-by-step through configuration.
  * **Scriptable Non-Interactive Mode**: All options can be passed as command-line arguments, making it perfect for automation and CI/CD pipelines.
  * **Rich Terminal Output**: Beautifully formatted summaries, spinners for long-running tasks, and clear feedback using Rich.
  * **Safe by Default**: Includes confirmation prompts for final actions to prevent accidental runs.
  * **Modern Python Tooling**: Built with Typer, Textual, and Rich, and packaged using modern `pyproject.toml` standards.

## Design Rationale

This project adheres to a strict set of modern tooling choices to deliver a best-in-class CLI experience:

  - **Typer**: Used as the core CLI framework for its simplicity, excellent help text generation, and automatic command-line completion. It eliminates boilerplate and encourages clean command structures.
  - **Textual**: Powers the interactive, full-screen configuration editor. It provides a rich, app-like experience within the terminal, guiding users through complex configuration without overwhelming them.
  - **Rich**: Used for all terminal output, including beautifully formatted text, panels, and spinners. It ensures that all feedback is clear, visually appealing, and easy to parse.
  - **Questionary**: Handles interactive prompts, such as the final confirmation step. It offers a user-friendly way to gather simple input.

This stack was chosen to create a tool that is both powerful for automation and inviting for interactive use.

## Installation

This project uses modern Python packaging. The recommended way to install it is in "editable" mode, which allows you to make changes to the code that are immediately reflected without reinstalling.

1.  Ensure you have Python 3.8+ installed.
2.  Clone this repository:
    ```bash
    git clone <your-repo-url>
    cd synthetic-cli
    ```
3.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4.  Install the project and its dependencies:
    ```bash
    pip install -e .
    ```

## Usage

Once installed, the `synthetic-cli` command will be available in your terminal.

### Interactive Mode

To launch the full-screen guided configuration, run the command without any arguments:

```bash
synthetic-cli
```

This will start the Textual-based interface, which will walk you through setting the use case, labels, and API key.

### Scripted Mode

For automation, provide all necessary configuration as command-line arguments.

```bash
synthetic-cli \
  --use-case "Text Classification" \
  --label "positive" \
  --label "negative" \
  --api-key "your-secret-api-key" \
  --output "classified_data.csv"
```

You can also set the API key via an environment variable for better security:

```bash
export SYNTH_API_KEY="your-secret-api-key"
synthetic-cli --use-case "Text Classification" --label "spam"
```

## Troubleshooting

Here are solutions to common issues that may arise during setup.

### `ModuleNotFoundError: No module named 'synthetic_cli'`

This error occurs if there is a mismatch between the directory name and the import statements.

  * **Solution**: Ensure your package directory uses an **underscore** (`synthetic_cli`) and not a hyphen. Hyphens are invalid in Python import names. All `import` statements in the code must also use the underscore (`from synthetic_cli...`). The `pyproject.toml` should also point to the correct module name in the `[project.scripts]` section.

### `ImportError: Package 'textual.widgets' has no class 'RadioButtons'`

This is caused by an update to the Textual library.

  * **Solution**: The `RadioButtons` widget was renamed to `RadioSet`. Open `synthetic_cli/tui/app.py` and change the import and usage from `RadioButtons` to `RadioSet`.

## Project Structure

The project is organized into logical modules for maintainability:

```
.
├── synthetic_cli/        # The Python package source code
│   ├── commands/         # Core logic for each CLI command
│   ├── config/           # Data models for configuration
│   ├── tui/              # Textual TUI application
│   └── cli.py            # Main Typer application entrypoint
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
```

## Contributing

Contributions are welcome\! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.