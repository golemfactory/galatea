"""
The requestor's agent controlling and interacting with the classifier vm
"""
import asyncio
from datetime import datetime, timedelta
import aiofiles
import random
import string
import os
from itertools import count

from yapapi import (
    Executor,
    Task,
    __version__ as yapapi_version,
    WorkContext,
)

from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.package import vm


async def service_start(yagna_app):
    # Set the Yagna's APP_KEY
    assert yagna_app and yagna_app["appkey"], "Classificator cannot be started, Yagna's APP_KEY is missing."
    os.environ["YAGNA_APPKEY"] = yagna_app["appkey"]

    timeout = timedelta(minutes=115)
    package = await vm.repo(
        image_hash=os.getenv("PROVIDER_IMAGE_HASH", "c6b743459d3428fb860582e556ceba1c76dbc8a1d599a55dcf73e437"),
        min_mem_gib=1.5,
        min_storage_gib=3.0,
    )

    async def handle_requests(ctx: WorkContext, tasks):
        """
        Initializes classifiers and yields texts as tasks
        """
        QUEUE_GET_TIMEOUT_SECONDS = 30
        text_queue = yagna_app["tasks"]

        ctx.run("/bin/sh", "-c", "nohup python classifier.py run &")
        yield ctx.commit()
        print("Activity initialized.")

        try:
            async for task in tasks:
                test_filename = f"sample_{task.data:08}.txt"

                text, fut = await asyncio.wait_for(text_queue.get(), QUEUE_GET_TIMEOUT_SECONDS)
                assert text, "Empty input not expected"
                print(f"Received text from queue: {text[:24]}...")

                input_file_path = f"/tmp/yagna-service-poc/{test_filename}.in"
                async with aiofiles.open(input_file_path, mode="w") as f:
                    await f.write(text)

                print("Sending input sample for classification " + input_file_path)
                ctx.send_file(input_file_path, f"/work/{test_filename}.in")
                ctx.run(
                    "/usr/local/bin/python", "classifier.py", "submit", f"/work/{test_filename}.in", f"/work/{test_filename}.out"
                )

                output_file_path = f"/tmp/yagna-service-poc/{test_filename}.out"
                ctx.download_file(f"/work/{test_filename}.out", output_file_path)
                yield ctx.commit(timeout=timeout)

                print("Received response to sample " + output_file_path)
                async with aiofiles.open(output_file_path, mode="r") as f:
                    fut.set_result(await f.read())

                text_queue.task_done()
                task.accept_result()

        except (KeyboardInterrupt, asyncio.CancelledError):
            # let's ignore errors and pretend nothing has happened
            pass
        except asyncio.TimeoutError:
            # let provider know that we need its resources
            print(f"No input received in iteration {task.data}")
            ctx.commit()
            task.accept_result()

    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Executor(
            package=package,
            max_workers=1,
            budget=10.0,
            timeout=timeout,
            subnet_tag=os.getenv("YAPAPI_SUBNET_TAG"),
            driver=os.getenv("YAPAPI_DRIVER", "zksync"),
            network=os.getenv("YAPAPI_NETWORK", "rinkeby"),
            event_consumer=log_summary(log_event_repr),
    ) as executor:

        print(
            f"yapapi version: {yapapi_version}\n"
            f"payment driver: {executor.driver}, "
            f"and network: {executor.network}\n"
        )

        start_time = datetime.now()

        async for task in executor.submit(handle_requests, (Task(data=n) for n in count(1))):
            print(
                f"Script executed: {task}, result: {task.result}, time: {task.running_time}"
            )

        print(
            f"Service finished, total time: {datetime.now() - start_time}"
        )


async def main():
    yagna_app = {
        "tasks": asyncio.Queue(),
        "appkey": os.getenv("YAGNA_APPKEY")
    }
    text = """
    The Queen has conducted her first in-person royal duty since her husband, the Duke of Edinburgh, died on Friday.
    The monarch hosted a ceremony in which the Earl Peel formally stood down as Lord Chamberlain, whose office organises royal ceremonies.
    During a private event held at Windsor Castle, the Queen accepted her former royal aide's wand and office insignia.
    The Royal Family is observing two weeks of mourning. The duke's funeral will take place at Windsor on Saturday.
    A royal official said members of the family would continue "to undertake engagements appropriate to the circumstances".
        """

    future = asyncio.get_running_loop().create_future()
    yagna_app["tasks"].put_nowait((text, future))

    asyncio.ensure_future(service_start(yagna_app))

    print("Requestor task started")
    await future
    print(future.result())
    print("DONE.")

if __name__ == "__main__":
    os.environ["YAPAPI_SUBNET_TAG"] = "galatea"

    enable_default_logger(
        log_file="service-yapapi.log",
        debug_activity_api=True,
        debug_market_api=False,
        debug_payment_api=False,
    )

    asyncio.run(main())
