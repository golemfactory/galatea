import sys

from transformers import pipeline


def download(model: str, save_directory: str) -> None:
    classifier = pipeline('sentiment-analysis', model=model)
    classifier.save_pretrained(save_directory)


if __name__ == '__main__':
    try:
        model, save_directory = sys.argv[1:]
    except ValueError:
        print(f"Usage: {sys.argv[0]} <model> <save_directory>")
        sys.exit(1)

    download(model, save_directory)
