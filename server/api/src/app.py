from quart import Quart, request
from quart_cors import cors

import classifier
import os

from utils import get_yagna_app_key


YAGNA_ACCOUNT, YAGNA_APP_KEY = "0x000000000000000000000000000000000000dEaD", "appkey_not_obtained"
if not os.getenv("NO_YAGNA"):
    # Wait for the `app_key` file is available in `yagna` directory. This file is created by yagna service init script.
    MAX_WAIT_TIME_SECONDS = 60
    PATH = "./yagna/app_key"
    YAGNA_ACCOUNT, YAGNA_APP_KEY = get_yagna_app_key(PATH, MAX_WAIT_TIME_SECONDS)


def create_app():
    app = Quart(__name__)
    cors(app)

    @app.route('/api')
    async def index():
        return {
            "version": "0.0.1",
            "git.commit": os.getenv("COMMIT", "0000000"),
            "git.branch": os.getenv("BRANCH", ""),
    }

    @app.route('/api/classify', methods=["POST"])
    async def classify():
        form = await request.form
        text = form.get("text_file") or form.get("text")
        print(text)

        return classifier.classify_text(text)


    return app
