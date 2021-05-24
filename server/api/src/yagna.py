import asyncio
import os
import time
from typing import TYPE_CHECKING

import aiofiles
import aiohttp

from utils import parse_yagna_key

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

MAX_WAIT_TIME_SECONDS = 60
APP_KEY_PATH = "./yagna/app_key"


class Yagna:
    def __init__(self) -> None:
        self.tasks = asyncio.Queue()
        self.account: 'Optional[str]' = None
        self.app_key: 'Optional[str]' = None
        self.rest_ready = False
        self.agreement_ready = False

    @property
    def initialized(self) -> bool:
        return bool(self.app_key)

    def as_dict(self) -> 'Dict[str, Any]':
        return {
            "yagna.initialized": self.initialized,
            "yagna.rest_ready": self.rest_ready,
            "yagna.agreement_ready": self.agreement_ready,
            "yagna.app_key": self.app_key,
            "yagna.account": self.account,
        }

    async def classify(self, text: str) -> str:
        fut = asyncio.get_running_loop().create_future()
        self.tasks.put_nowait((text, fut))
        return await fut

    async def wait_until_ready(self) -> None:
        await self._wait_for_app_key()
        await self._wait_for_rest()

    async def _wait_for_app_key(self) -> None:
        """
        Wait for the `app_key` file is available in `yagna` directory.
        This file is created by yagna service init script.
        """
        print(f"Waiting for Yagna service ready... (allowing {MAX_WAIT_TIME_SECONDS} secs)")
        deadline = time.time() + MAX_WAIT_TIME_SECONDS
        while time.time() < deadline:
            await asyncio.sleep(3)
            print("Checking for app_key file...")
            try:
                async with aiofiles.open(APP_KEY_PATH, mode="r") as f:
                    self.account, self.app_key = parse_yagna_key(await f.read())
                    break
            except FileNotFoundError:
                pass
        else:
            raise RuntimeError("Timeout: Yagna APP_KEY not found")

    async def _wait_for_rest(self) -> None:
        """
        Check if Yagna service responds to REST requests
        """
        assert self.initialized, "Yagna's app_key hasn't been read yet!"

        async with aiohttp.ClientSession() as session:

            payment_url = os.environ["YAGNA_API_URL"] + "/payment-api/v1/requestorAccounts"
            auth_header = {"Authorization": f"Bearer {self.app_key}"}

            while True:
                try:
                    async with session.get(payment_url, headers=auth_header) as response:
                        response = await response.json()
                        print(f"Trying to get requestors {response=}")
                        if response:
                            break
                        await asyncio.sleep(3)
                except Exception as ex:
                    print("Yagna ready exception " + str(ex))
                    await asyncio.sleep(5)
                    print("Retrying...")

        requestor, *_ = response
        self.rest_ready = requestor['address'] == self.account
