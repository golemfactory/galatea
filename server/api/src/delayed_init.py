import asyncio
import aiofiles
import aiohttp
import os

from utils import parse_yagna_key
from classifier import service_start
from time import time


async def is_yagna_available(yagna_app):
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
                account, appkey = parse_yagna_key(await f.read())
                yagna_app["account"] = account
                yagna_app["appkey"] = appkey

                break
        except FileNotFoundError:
            pass


async def is_yagna_ready(yagna_app):
    assert yagna_app and yagna_app["appkey"], "Yagna's appkey hasn't been read yet!"

    # Before we switch to YaPAPI let's first check if Yagna service responds tp REST requests
    async with aiohttp.ClientSession() as session:

        payment_url = os.environ["YAGNA_API_URL"] + "/payment-api/v1/requestorAccounts"
        yagna_appkey = yagna_app["appkey"]
        auth_header = {"Authorization": f"Bearer {yagna_appkey}"}

        while True:
            try:
                async with session.get(payment_url, headers=auth_header) as response:
                    response = await response.json()
                    print(f"Trying to get requestors {response=}")
                    if response: break
                    await asyncio.sleep(3)
            except Exception as ex:
                print("Yagna ready exception " + str(ex))
                await asyncio.sleep(5)
                print("Retrying...")

    requestor, *_ = response
    yagna_app["rest_ready"] = requestor['address'] == yagna_app["account"]


async def delayed_init(yagna_app):
    try:
        await is_yagna_available(yagna_app)
        await is_yagna_ready(yagna_app)

        # Start Yagna's service loop
        await service_start(yagna_app)

    except Exception as ex:
        print("Unable to connect with Yagna service" + str(ex))
