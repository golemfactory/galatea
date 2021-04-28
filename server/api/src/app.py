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
            "yagna.available": bool(app.yagna["appkey"]),
            "yagna.ready": app.yagna["ready"],
            "yagna.appkey": app.yagna["appkey"],
            "yagna.account": app.yagna["account"],
        }

    @app.route('/api/classify', methods=["POST"])
    async def classify():
        form = await request.form
        text = form.get("text_file") or form.get("text")
        print(text)

        text_queue = app.yagna["tasks"]
        fut = asyncio.get_running_loop().create_future()
        text_queue.put_nowait((text, fut))

        await fut
        # TODO: Future can be cancelled...
        return fut.result()

    @app.before_serving
    async def init_wait_yagna():
        app.yagna = {
            "account": None,
            "appkey": None,
            "ready": False,
            "tasks": asyncio.Queue()
        }

        asyncio.ensure_future(delayed_init(app.yagna))

    return app
