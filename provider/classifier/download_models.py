import json
from pathlib import Path
from typing import TYPE_CHECKING

import click
from transformers import pipeline

if TYPE_CHECKING:
    from typing import Dict, Any, TextIO


@click.command()
@click.argument('models_json', envvar='MODELS_JSON', type=click.File())
@click.argument('models_dir', envvar='MODELS_DIR', type=click.Path(file_okay=False, writable=True))
def download_models(models_json: 'TextIO', models_dir: str) -> None:
    models: Dict[str, Dict[str, Any]] = json.load(models_json)
    save_directory = Path(models_dir)
    for (model_name, model_def) in models.items():
        download_model(model_def['task'], model_def['ref'], save_directory / model_name)
    print("All models downloaded.")


def download_model(task: str, model: str, save_directory: Path) -> None:
    print(f"Downloading model '{model}' into '{save_directory}'...", end=' ', flush=True)
    classifier = pipeline(task, model=model)
    classifier.save_pretrained(save_directory)
    print("Done.")


if __name__ == '__main__':
    download_models()
