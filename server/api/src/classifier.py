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

package = await vm.repo(
    image_hash="c6b743459d3428fb860582e556ceba1c76dbc8a1d599a55dcf73e437",
    min_mem_gib=0.5,
    min_storage_gib=4.0,
)


async def service_start(yagna_app):
    # Set the Yagna's APP_KEY
    assert yagna_app and yagna_app["appkey"], "Classificator cannot be started, Yagna's APP_KEY is missing."
    os.environ["YAGNA_APPKEY"] = yagna_app["appkey"]

    async def handle_requests(ctx: WorkContext, tasks):
        """
        Initializes classifiers and yields texts as tasks
        """
        PYTHON = "/usr/lib/python"
        CLASSIFIER_SCRIPT = "/classifier/classifier.py"
        QUEUE_GET_TIMEOUT_SECONDS = 30

        # Wait on queue until timeout to make provider busy
        text_queue = yagna_app["tasks"]

        ctx.run(f"{PYTHON} {CLASSIFIER_SCRIPT}", "run")

        yield ctx.commit()

        try:
            while True:
                test_filename = (
                        "".join(random.choice(string.ascii_letters) for _ in range(10)) + ".txt"
                )

                text, fut = asyncio.wait_for(text_queue.get(), QUEUE_GET_TIMEOUT_SECONDS)
                counter = task.data

                ctx.send_bytes(f"/work/{test_filename}.in", text.encode())
                ctx.run(
                    f"{PYTHON} {CLASSIFIER_SCRIPT} submit /work/{test_filename}.in /work/{test_filename}.out"
                )

                yield ctx.commit()

                ctx.download_file(f"/work/{test_filename}.out", f"/tmp/{test_filename}")
                yield ctx.commit()

                async with aiofiles.open(f"/tmp/{test_filename}", mode="r") as f:
                    fut.set_result(await f.read())

                text_queue.task_done()
                task.accept_result()

        except asyncio.CancelledError:
            # let's ignore errors and pretend nothing has happened
            pass
        except asyncio.TimeoutError:
            # let provider know that we need its resources
            ctx.commit()

    timeout = timedelta(minutes=29)

    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Executor(
            package=package,
            max_workers=1,
            budget=1.0,
            timeout=timeout,
            subnet_tag=os.getenv("YAPAPI_SUBNET_TAG"),
            driver=os.getenv("YAPAPI_DRIVER"),
            network=os.getenv("YAPAPI_NETWORK"),
            event_consumer=log_summary(log_event_repr),
    ) as executor:

        print(
            f"yapapi version: {yapapi_version}\n"
            f"Using subnet: {subnet_tag}, "
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
