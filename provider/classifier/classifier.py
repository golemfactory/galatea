import json
from pathlib import Path
from typing import TYPE_CHECKING

import click
import zmq
from transformers import pipeline

if TYPE_CHECKING:
    from io import BytesIO
    from typing import TextIO, Dict, Callable, Any


SOCKET_ADDR = "ipc:///tmp/classifier.sock"  # TODO: Allow configuration (env var)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('models_json', envvar='MODELS_JSON', type=click.File())
@click.argument('models_dir', envvar='MODELS_DIR', type=click.Path(exists=True, file_okay=False, readable=True))
def run(models_json: 'TextIO', models_dir: str) -> None:
    print("Loading models...", end=' ', flush=True)
    classifiers = load_models(models_json, Path(models_dir))
    print("Done.")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(SOCKET_ADDR)
    print(f"Server listening on socket {SOCKET_ADDR}...")

    while True:
        msg: bytes = socket.recv()
        try:
            text = msg.decode()
            result = run_classifiers(classifiers, text)
            reply = json.dumps(result).encode()
        except Exception as e:
            reply = f"ERROR: {e}".encode()
        socket.send(reply)


@cli.command()
@click.argument('input_file', type=click.File(mode='rb'))
@click.argument('output_file', type=click.File(mode='wb'))
def submit(input_file: 'BytesIO', output_file: 'BytesIO') -> None:
    msg = input_file.read()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(SOCKET_ADDR)
    socket.send(msg)
    reply = socket.recv()
    output_file.write(reply)


def load_models(models_json: 'TextIO', models_dir: Path) -> 'Dict[str, Callable]':
    models: Dict[str, Dict[str, Any]] = json.load(models_json)
    return {
        model_name: pipeline(
            task=model_def['task'],
            model=str(models_dir / model_name),
            **model_def['pipeline_params']
        )
        for model_name, model_def in models.items()
    }


def run_classifiers(classifiers: 'Dict[str, Callable]', text: str) -> 'Dict[str, Any]':
    # TODO: Make it parallel
    return {
        model_name: classifier(text)[0]
        for model_name, classifier in classifiers.items()
    }


if __name__ == '__main__':
    cli()
