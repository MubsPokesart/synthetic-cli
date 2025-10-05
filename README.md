# Synthetic Data Generation CLI

A minimal, production-grade command-line tool for interactively configuring and running synthetic data generation tasks. This tool is built with a human-first design philosophy, prioritizing an intuitive and robust user experience.

## Features

* **Interactive TUI Mode**: A full-screen terminal interface, powered by Textual, guides you step-by-step through configuration.
* **Hugging Face Integration**: Leverages the `transformers` library to generate high-quality synthetic data using models from the Hugging Face Hub.
* **Rich Terminal Output**: Beautifully formatted summaries, spinners for long-running tasks, and clear feedback using Rich.
* **Modern Python Tooling**: Built with Typer, Textual, and Rich, and packaged using modern `pyproject.toml` standards.

## Design Rationale

This project adheres to a strict set of modern tooling choices to deliver a best-in-class CLI experience:

- **Typer**: Used as the core CLI framework for its simplicity, excellent help text generation, and automatic command-line completion.
- **Textual**: Powers the interactive, full-screen configuration editor, providing a rich, app-like experience within the terminal.
- **Rich**: Used for all terminal output, ensuring that all feedback is clear, visually appealing, and easy to parse.
- **Hugging Face `transformers`**: The core of the data generation, providing access to a vast library of state-of-the-art language models.

## Installation

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
    pip install -r requirements.txt
    pip install -e .
    ```

## Usage

Once installed, the `synthetic-cli` command will be available in your terminal.

To launch the full-screen guided configuration, run the command without any arguments:

```bash
synthetic-cli
```

This will start the Textual-based interface, which will walk you through setting the use case, labels, categories, and other generation parameters. You will also be prompted to enter your Hugging Face token, which is required to download and use the models.

## Project Structure

The project is organized into logical modules for maintainability:

```
.
├── synthetic_cli/        # The Python package source code
│   ├── commands/         # Core logic for each CLI command
│   ├── config/           # Data models for configuration
│   ├── tui/              # Textual TUI application
│   │   └── screens/      # Individual screens for the TUI
│   └── cli.py            # Main Typer application entrypoint
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
