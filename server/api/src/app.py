from quart import Quart, request
from quart_cors import cors

import classifier
import os

from utils import get_yagna_app_key


YAGNA_ACCOUNT, YAGNA_APP_KEY = "0x000000000000000000000000000000000000dEaD", "appkey_not_obtained"


async def get_requestor_accounts():
    # Alright, this will serve just as a demo that API is able to connect to yagna service
    # This code will be reorganized latter... most likely with a help of yapapi SDK
    import aiohttp
    from asyncio import sleep

    async with aiohttp.ClientSession() as session:
        payment_url = os.environ["YAGNA_URL"] + "payment-api/v1/requestorAccounts"
        auth_header = {"Authorization": f"Bearer {YAGNA_APP_KEY}"}

        while True:
            async with session.get(payment_url, headers=auth_header) as response:
                response = await response.json()
                print(f"Trying to get requestors {response=}")
                if response: break
                await sleep(3)

    [requestor] = response
    assert requestor['address'] == YAGNA_ACCOUNT, "Account don't match"


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

    @app.before_serving
    async def init_wait_yagna():
        global  YAGNA_ACCOUNT, YAGNA_APP_KEY
        if not os.getenv("NO_YAGNA"):
            # Wait for the `app_key` file is available in `yagna` directory. This file is created by yagna service init script.
            MAX_WAIT_TIME_SECONDS = 60
            PATH = "./yagna/app_key"
            YAGNA_ACCOUNT, YAGNA_APP_KEY = get_yagna_app_key(PATH, MAX_WAIT_TIME_SECONDS)

            await get_requestor_accounts()

    return app
