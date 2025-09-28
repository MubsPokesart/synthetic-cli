# Synthetic Data Generation CLI

A minimal, production-grade command-line tool for interactively configuring and running synthetic data generation tasks. This tool is built with a human-first design philosophy, prioritizing an intuitive and robust user experience.

## Design Rationale

This project adheres to a strict set of modern tooling choices to deliver a best-in-class CLI experience:

-   **Typer**: Used as the core CLI framework for its simplicity, excellent help text generation, and automatic command-line completion. It eliminates boilerplate and encourages clean command structures.
-   **Textual**: Powers the interactive, full-screen configuration editor. It provides a rich, app-like experience within the terminal, guiding users through complex configuration without overwhelming them.
-   **Rich**: Used for all terminal output, including beautifully formatted text, panels, and spinners. It ensures that all feedback is clear, visually appealing, and easy to parse.
-   **Questionary**: Handles interactive prompts, such as the final confirmation step. It offers a user-friendly way to gather simple input and is more polished than basic `input()`.

This stack was chosen to create a tool that is both powerful for automation and inviting for interactive use.

## Installation

1.  Ensure you have Python 3.8+ installed.
2.  Clone this repository or download the source files.
3.  Install the required dependencies:

```bash
pip install -r requirements.txt
```