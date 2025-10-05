"""
Contains the core logic for the 'generate' command, orchestrating the
synthetic data generation process.
"""

import os
import re
import random
from datetime import datetime
from typing import Tuple, List, Dict

import pandas as pd
from rich.console import Console
from huggingface_hub import login
from transformers import pipeline, AutoTokenizer

from synthetic_cli.config.models import GenerationConfig

console = Console()

class DataGenerator:
    """Manages the synthetic data generation lifecycle."""

    def __init__(self, config: GenerationConfig):
        self.config = config
        self.tokenizer = None
        self.generator = None

    def _login_to_hf(self):
        """Logs into Hugging Face using the provided token."""
        token = self.config.model_config.hf_token
        if not token:
            console.print("[bold red]Error: Hugging Face token is not provided.[/bold red]")
            raise ValueError("HF_TOKEN is required.")
        login(token)

    def _initialize_pipeline(self):
        """Initializes the tokenizer and text generation pipeline."""
        console.print(f"[bold blue]Initializing model: {self.config.model_config.model}...[/bold blue]")
        self._login_to_hf()
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_config.model)
        self.generator = pipeline(
            "text-generation",
            model=self.config.model_config.model,
            tokenizer=self.tokenizer,
        )

    def _parse_output(self, text: str) -> Tuple[str, str]:
        """Parses the model's output to extract the generated text and reasoning."""
        match = re.search(r"OUTPUT:\s*(.+?)\s*REASONING:\s*(.+)", text, re.DOTALL)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        
        match = re.search(r"output:\s*(.+?)\s*reasoning:\s*(.+)", text, re.DOTALL | re.IGNORECASE)
        if match:
            console.print("[yellow]Warning: Model used lowercase format.[/yellow]")
            return match.group(1).strip(), match.group(2).strip()

        match = re.search(r"OUTPUT:\s*(.+)", text, re.DOTALL)
        if match:
            console.print("[yellow]Warning: No REASONING found.[/yellow]")
            return match.group(1).strip(), "No reasoning provided"

        console.print("[yellow]Warning: Response format not recognized. Using raw output.[/yellow]")
        return text.strip(), "Format not recognized"

    def _build_prompt(self, label: str, category: str, type_name: str) -> str:
        """Constructs the prompt for the language model."""
        return f"""You should create synthetic data for specified labels and categories.
        This is especially useful for {self.config.use_case_config.use_case}.

        *Label Descriptions*
        {self.config.use_case_config.label_descriptions}

        *Examples*
        {self.config.use_case_config.prompt_examples}

        ####################

        Generate one output for the classification below.
        You may use the examples I have provided as a guide, but you cannot simply modify or rewrite them.
        Only return the OUTPUT and REASONING.
        Do not return the LABEL, CATEGORY, or TYPE.

        LABEL: {label}
        CATEGORY: {category}
        TYPE: {type_name}
        OUTPUT:
        REASONING:
        """

    def _generate_sample(self, label: str, category: str, type_name: str) -> Tuple[str, str]:
        """Generates a single data sample."""
        prompt = self._build_prompt(label, category, type_name)
        messages = [
            {
                "role": "system",
                "content": f"You are a helpful assistant designed to generate synthetic data for {self.config.use_case_config.use_case}."
            },
            {"role": "user", "content": prompt},
        ]
        
        result = self.generator(messages, max_new_tokens=self.config.model_config.max_new_tokens)[0]["generated_text"][-1]["content"]
        return self._parse_output(result)

    def run(self):
        """Executes the full data generation process."""
        self._initialize_pipeline()
        
        output_conf = self.config.output_config
        use_case_conf = self.config.use_case_config
        model_conf = self.config.model_config

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_conf.output_dir, exist_ok=True)
        output_path = os.path.join(output_conf.output_dir, f"{timestamp}.csv")

        num_batches = (output_conf.sample_size + output_conf.batch_size - 1) // output_conf.batch_size
        console.print(f"[bold green]Starting generation of {output_conf.sample_size} samples in {num_batches} batches...[/bold green]")

        for batch_num in range(num_batches):
            batch_data = []
            start_index = batch_num * output_conf.batch_size
            end_index = min(start_index + output_conf.batch_size, output_conf.sample_size)

            for i in range(start_index, end_index):
                label = random.choice(use_case_conf.labels)
                category = random.choice(list(use_case_conf.categories_types.keys()))
                type_name = random.choice(use_case_conf.categories_types[category])

                text, reasoning = self._generate_sample(label, category, type_name)
                
                entry = {"text": text, "label": label, "model": model_conf.model}
                if output_conf.save_reasoning:
                    entry["reasoning"] = reasoning
                batch_data.append(entry)

            batch_df = pd.DataFrame(batch_data)
            if batch_num == 0:
                batch_df.to_csv(output_path, mode='w', index=False)
            else:
                batch_df.to_csv(output_path, mode='a', header=False, index=False)
            
            console.print(f"[cyan]Batch {batch_num + 1}/{num_batches} saved to {output_path}[/cyan]")

        console.print(f"[bold green]Data generation complete. Output saved to {output_path}[/bold green]")

def generate_data(config: GenerationConfig):
    """Initializes and runs the data generator."""
    if not config.is_valid():
        console.print("[bold red]Configuration is invalid. Please check your settings.[/bold red]")
        return

    generator = DataGenerator(config)
    generator.run()
