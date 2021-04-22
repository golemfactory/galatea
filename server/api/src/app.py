from flask import Flask, request
from flask_cors import CORS

import classifier
import os
from pathlib import Path
from time import sleep, time

# Wait for the `app_key` file is available in `yagna` directory. This file is created by yagna service init script.
MAX_WAIT_TIME_SECONDS = 60
wait_start = time()
path = Path("./yagna/app_key")

print(f"Waiting for Yagna service ready... (allowing {MAX_WAIT_TIME_SECONDS} secs)")
while not path.exists():
    sleep(1)
    assert time() - wait_start < MAX_WAIT_TIME_SECONDS, "Yagna service was not ready in the time period."

YAGNA_APP_KEY = path.read_text().strip()
print(f"{YAGNA_APP_KEY=}")
assert len(YAGNA_APP_KEY) == 32, "Unable to read Yagna app key."


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.route('/api')
    def index():
        return {
            "version": "0.0.1",
            "git.commit": os.getenv("COMMIT", "0000000"),
            "git.branch": os.getenv("BRANCH", ""),
    }

    @app.route('/api/classify', methods=["POST"])
    def classify():
        text = request.form.get("text_file") or request.form.get("text")
        print(text)

        return classifier.classify_text(text)


    return app
