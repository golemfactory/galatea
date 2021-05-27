import asyncio
import os

from quart import Quart, request
from quart_cors import cors

from classifier import service_start
from yagna import Yagna


def create_app():
    app = Quart(__name__)
    cors(app)

    @app.route('/api')
    async def index():
        version_info = {
            "version": "0.0.1",
            "git.commit": os.getenv("COMMIT", "0000000"),
            "git.branch": os.getenv("BRANCH", ""),
        }
        version_info.update(app.yagna.as_dict())
        return version_info

    @app.route('/api/classify', methods=["POST"])
    async def classify():
        form = await request.form
        text = form.get("text_file") or form.get("text")
        print("/api/classify: Received text for classification")
        print(f"{text[:24]}...")

        print("/api/classify: Waiting for classifier answer")
        return await app.yagna.classify(text)  # TODO: Handle classifier errors

    @app.before_serving
    async def init_wait_yagna():
        app.yagna = Yagna()
        await app.yagna.wait_until_ready()
        asyncio.ensure_future(service_start(app.yagna))

    return app
