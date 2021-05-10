from quart import Quart, request
from quart_cors import cors

import asyncio
import os

from delayed_init import delayed_init


def create_app():
    app = Quart(__name__)
    cors(app)

    @app.route('/api')
    async def index():
        return {
            "version": "0.0.1",
            "git.commit": os.getenv("COMMIT", "0000000"),
            "git.branch": os.getenv("BRANCH", ""),
            "yagna.initialized": bool(app.yagna["appkey"]),
            "yagna.rest_ready": app.yagna["rest_ready"],
            "yagna.aggr_ready": app.yagna["aggr_ready"],
            "yagna.appkey": app.yagna["appkey"],
            "yagna.account": app.yagna["account"],
        }

    @app.route('/api/classify', methods=["POST"])
    async def classify():
        form = await request.form
        text = form.get("text_file") or form.get("text")
        print("/api/classify: Received text for classification")
        print(f"{text[:24]}...")

        text_queue = app.yagna["tasks"]
        fut = asyncio.get_running_loop().create_future()
        text_queue.put_nowait((text, fut))

        print("/api/classify: Waiting for classificator answer")
        await fut
        # TODO: Future can be cancelled...
        return fut.result()

    @app.before_serving
    async def init_wait_yagna():
        app.yagna = {
            "account": None,
            "tasks": asyncio.Queue(),

            # after APP_KEY is obtained it sets `yagna.initialized`
            "appkey": None,

            # after first rest request to yagna demon is successful it sets `yagna.rest_ready`
            "rest_ready": False,

            # after agreement with provider is ready it sets `yagna.aggr_ready`
            "aggr_ready": False,

        }

        asyncio.ensure_future(delayed_init(app.yagna))

    return app
