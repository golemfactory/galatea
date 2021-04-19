import sys

from transformers import pipeline


def download(task: str, model: str, save_directory: str) -> None:
    classifier = pipeline(task, model=model)
    classifier.save_pretrained(save_directory)


if __name__ == '__main__':
    try:
        task, model, save_directory = sys.argv[1:]
    except ValueError:
        print(f"Usage: {sys.argv[0]} <task> <model> <save_directory>")
        sys.exit(1)

    download(task, model, save_directory)
