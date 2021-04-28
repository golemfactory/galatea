from quart import Quart, request
from quart_cors import cors

import asyncio
import classifier
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
            "yagna.available": hasattr(app, "yagna_available") and app.yagna_available,
            "yagna.ready": hasattr(app, "yagna_ready") and app.yagna_ready,
        }

    @app.route('/api/classify', methods=["POST"])
    async def classify():
        form = await request.form
        text = form.get("text_file") or form.get("text")
        print(text)

        return classifier.classify_text(text)

    @app.before_serving
    async def init_wait_yagna():
        if not hasattr(app, "yagna_available"):
            app.yagna_available = False

        if not hasattr(app, "yagna_ready"):
            app.yagna_ready = False

        asyncio.ensure_future(delayed_init(app))

    return app
