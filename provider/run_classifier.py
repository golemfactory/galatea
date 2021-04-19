import sys
from pathlib import Path

from transformers import pipeline


def run(task: str, model: str, input_path: Path, output_path: Path) -> None:
    kwargs = {'return_all_scores': True} if task == 'sentiment-analysis' else {}
    classifier = pipeline(task, model=model, **kwargs)
    text = input_path.read_text(encoding="utf-8")
    result = classifier(text)
    if task == 'sentiment-analysis':
        result_str = str({item['label']: item['score'] for item in result[0]})
    elif task == 'summarization':
        result_str = result[0]['summary_text']
    else:
        result_str = str(result)
    output_path.write_text(result_str, encoding="utf-8")


if __name__ == '__main__':
    try:
        task, model, input_path, output_path = sys.argv[1:]
        input_path = Path(input_path)
        output_path = Path(output_path)
    except (ValueError, TypeError):
        print(f"Usage: {sys.argv[0]} <task> <model> <input> <output>")
        sys.exit(1)

    assert input_path.is_file(), f"{input_path} is not a file"
    assert output_path.parent.is_dir(), f"{output_path.parent} is not a directory"

    run(task, model, input_path, output_path)
