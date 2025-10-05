"""
Defines the data structures for managing configuration state.

These dataclasses provide type safety and a clear source of truth for the
application's configuration, separating concerns into logical groups.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class UseCaseConfig:
    """Configuration for the use case and prompt structure."""
    use_case: str = "text classification"
    labels: List[str] = field(default_factory=list)
    label_descriptions: str = ""
    categories_types: Dict[str, List[str]] = field(default_factory=dict)
    prompt_examples: str = ""

@dataclass
class ModelConfig:
    """Configuration for the language model and generation parameters."""
    model: str = "meta-llama/Llama-3.2-3B-Instruct"
    max_new_tokens: int = 256
    hf_token: Optional[str] = None

@dataclass
class OutputConfig:
    """Configuration for the output and processing."""
    sample_size: int = 100
    batch_size: int = 20
    output_dir: str = "./generated_data"
    save_reasoning: bool = True

@dataclass
class GenerationConfig:
    """Top-level container for all data generation configurations."""
    use_case_config: UseCaseConfig = field(default_factory=UseCaseConfig)
    model_config: ModelConfig = field(default_factory=ModelConfig)
    output_config: OutputConfig = field(default_factory=OutputConfig)

    def is_valid(self) -> bool:
        """Checks if the core configuration fields are populated."""
        return all([
            self.use_case_config.use_case,
            self.use_case_config.labels,
            self.use_case_config.categories_types,
            self.model_config.model,
            self.output_config.output_dir
        ])
