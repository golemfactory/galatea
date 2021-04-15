import sys
from pathlib import Path

from transformers import pipeline


def run(model: str, input_path: Path, output_path: Path) -> None:
    classifier = pipeline('sentiment-analysis', model=model, return_all_scores=True)
    text = input_path.read_text(encoding="utf-8")
    result = classifier(text)
    result_str = str({item['label']: item['score'] for item in result[0]})
    output_path.write_text(result_str, encoding="utf-8")


if __name__ == '__main__':
    try:
        model, input_path, output_path = sys.argv[1:]
        input_path = Path(input_path)
        output_path = Path(output_path)
    except (KeyError, TypeError):
        print(f"Usage: {sys.argv[0]} <model> <input> <output>")
        sys.exit(1)

    assert input_path.is_file(), f"{input_path} is not a file"
    assert output_path.parent.is_dir(), f"{output_path.parent} is not a directory"

    run(model, input_path, output_path)
