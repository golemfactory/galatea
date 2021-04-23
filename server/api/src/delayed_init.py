import asyncio
import aiofiles
import aiohttp
import os

from utils import parse_yagna_key
from time import time

async def is_yagna_available(app):
    global YAGNA_ACCOUNT, YAGNA_APP_KEY
    # Wait for the `app_key` file is available in `yagna` directory. This file is created by yagna service init script.
    MAX_WAIT_TIME_SECONDS = 60
    PATH = "./yagna/app_key"

    print(f"Waiting for Yagna service ready... (allowing {MAX_WAIT_TIME_SECONDS} secs)")
    wait_start = time()
    while True:
        await asyncio.sleep(3)
        assert time() - wait_start < MAX_WAIT_TIME_SECONDS, "Timeout: Yagna APP_KEY not found"
        print("Checking for app_Key file...")
        try:
            async with aiofiles.open(PATH, mode="r") as f:
                YAGNA_ACCOUNT, YAGNA_APP_KEY = parse_yagna_key(await f.read())
                app.yagna_available = True
                break
        except FileNotFoundError:
            app.yagna_available = False


async def is_yagna_ready(app):
    # Alright, this will serve just as a demo that API is able to connect to yagna service
    # This code will be reorganized latter... most likely with a help of yapapi SDK
    async with aiohttp.ClientSession() as session:
        payment_url = os.environ["YAGNA_URL"] + "payment-api/v1/requestorAccounts"
        auth_header = {"Authorization": f"Bearer {YAGNA_APP_KEY}"}

        while True:
            async with session.get(payment_url, headers=auth_header) as response:
                response = await response.json()
                print(f"Trying to get requestors {response=}")
                if response: break
                await asyncio.sleep(3)

    requestor, *_ = response
    app.yagna_ready = requestor['address'] == YAGNA_ACCOUNT


async def delayed_init(app):
    try:
        await is_yagna_available(app)
        await is_yagna_ready(app)
    except Exception as ex:
        print("Unable to connect with Yagna service" + str(ex))
