"""
Defines the data structures for managing configuration state.

Using a dataclass provides type safety and a clear, single source of
truth for the application's configuration state, which is passed
between the TUI, command-line arguments, and business logic.
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class GenerationConfig:
    """Holds all configuration parameters for a data generation task."""
    use_case: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    examples_per_label: int = 50
    model: str = "gpt-4-turbo"
    api_key: Optional[str] = None
    output_path: str = "./synthetic_data.csv"

    def is_valid(self) -> bool:
        """Checks if the core configuration fields are populated."""
        return all([
            self.use_case,
            self.labels,
            self.api_key
        ])