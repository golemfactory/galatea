"""
The requestor's agent controlling and interacting with the classifier vm
"""
import asyncio
from datetime import datetime, timedelta
import aiofiles
import os
import uuid
from typing import List, Optional, Set, Tuple

from yapapi import (
    Executor,
    Task,
    __version__ as yapapi_version,
    WorkContext,
)

from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.package import vm
from yapapi.executor.strategy import (DummyMS, SCORE_REJECTED)

from yagna import Yagna

CLASSIFIER_WORK_DIR = "/work"
PROVIDER_IMAGE_HASH = "6098588119b9483b099af3ffc1e9247cd6d14e6a4d34eec36cd8119a"

class DenylistMS(DummyMS):
    def __init__(self, providers: List[str]) -> None:
        self._providers: Set[str] = set(providers)

    async def score_offer(self, offer, *args, **kwargs) -> float:
        if offer.issuer in self._providers:
            return SCORE_REJECTED
        return await super().score_offer(offer, *args, **kwargs)


async def handle_requests(ctx: WorkContext, tasks):
    """
    Initializes classifiers and yields texts as tasks
    """
    task = await tasks.__anext__()
    text_queue = task.data.tasks

    try:
        copy_models(ctx)
        ctx.run("/bin/sh", "-c", "nohup python classifier.py run &")
        yield ctx.commit(timeout=timedelta(minutes=50))
        print("Models transfer completed")
        print("Activity initialized.")

        while True:
            test_filename = f"sample_{uuid.uuid4().hex}.txt"

            text, fut = await text_queue.get()
            assert text, "Empty input not expected"
            print(f"Received text from queue: {text[:24]}...")

            input_file_path = f"./{test_filename}.in"
            async with aiofiles.open(input_file_path, mode="w") as f:
                await f.write(text)

            print("Sending input sample for classification " + input_file_path)
            ctx.send_file(input_file_path, f"/work/{test_filename}.in")
            ctx.run(
                "/usr/local/bin/python", "classifier.py", "submit",
                f"/work/{test_filename}.in",
                f"/work/{test_filename}.out"
            )

            output_file_path = f"./{test_filename}.out"
            ctx.download_file(f"/work/{test_filename}.out", output_file_path)
            yield ctx.commit(timeout=timedelta(minutes=25))

            print("Received response to sample " + output_file_path)
            async with aiofiles.open(output_file_path, mode="r") as f:
                fut.set_result(await f.read())

    except (KeyboardInterrupt, asyncio.CancelledError, asyncio.TimeoutError):
        yield ctx.commit()
        task.accept_result()


def copy_models(ctx):
    print("Models transfer started")
    ctx.send_file("./models.json", f"{CLASSIFIER_WORK_DIR}/models.json")

    for path, _subdir, files in os.walk("models"):
        for file in files:
            print(f"Transfer file: {path}/{file}")
            ctx.send_file(f"{path}/{file}", f"{CLASSIFIER_WORK_DIR}/{path}/{file}")



async def service_start(yagna_app: Yagna) -> None:
    # Set the Yagna's APP_KEY
    assert yagna_app.initialized, "Classificator cannot be started, Yagna's APP_KEY is missing."
    os.environ["YAGNA_APPKEY"] = yagna_app.app_key

    package = await vm.repo(
        image_hash=os.getenv("PROVIDER_IMAGE_HASH", PROVIDER_IMAGE_HASH),
        min_mem_gib=1.5,
        min_storage_gib=2.0,
    )

    enable_default_logger(
        log_file="service-yapapi.log",
        debug_activity_api=True,
        debug_market_api=False,
        debug_payment_api=False,
    )

    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    print(
        "Starting YaPAPI Executor...\n"
        f"network:    {os.getenv('YAPAPI_NETWORK')}\n"
        f"driver:     {os.getenv('YAPAPI_DRIVER')}\n"
        f"subnet:     {os.getenv('YAPAPI_SUBNET_TAG')}\n"
        f"yagna url:  {os.getenv('YAGNA_API_URL')}\n"
    )
    async with Executor(
            package=package,
            max_workers=1,
            budget=10.0,
            timeout=timedelta(minutes=99),
            subnet_tag=os.getenv("YAPAPI_SUBNET_TAG"),
            driver=os.getenv("YAPAPI_DRIVER", "zksync"),
            network=os.getenv("YAPAPI_NETWORK", "rinkeby"),
            event_consumer=log_summary(log_event_repr),
            strategy=DenylistMS(os.getenv("DENY_LIST", "").split())
    ) as executor:
        print(
            f"yapapi version: {yapapi_version}\n"
            f"payment driver: {executor.driver}, "
            f"and network: {executor.network}\n"
        )

        start_time = datetime.now()
        yagna_app.agreement_ready = True

        async for task in executor.submit(handle_requests, (Task(data=yagna_app),)):
            print(
                f"Script executed: {task}, result: {task.result}, time: {task.running_time}"
            )

        print(
            f"Service finished, total time: {datetime.now() - start_time}"
        )


async def main():
    yagna_app = Yagna()
    yagna_app.app_key = os.getenv("YAGNA_APPKEY")
    text = """
    The Queen has conducted her first in-person royal duty since her husband, the Duke of Edinburgh, died on Friday.
    The monarch hosted a ceremony in which the Earl Peel formally stood down as Lord Chamberlain, whose office organises royal ceremonies.
    During a private event held at Windsor Castle, the Queen accepted her former royal aide's wand and office insignia.
    The Royal Family is observing two weeks of mourning. The duke's funeral will take place at Windsor on Saturday.
    A royal official said members of the family would continue "to undertake engagements appropriate to the circumstances".
        """

    future = asyncio.ensure_future(yagna_app.classify(text))
    asyncio.ensure_future(service_start(yagna_app))

    print("Requestor task started")
    await future
    print(future.result())
    print("DONE.")


if __name__ == "__main__":
    asyncio.run(main())
