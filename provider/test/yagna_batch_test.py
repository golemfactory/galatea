import asyncio
from datetime import timedelta
import pathlib

import click
from yapapi import Executor, Task, WorkContext
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.package import vm

INPUT_PATH = str(pathlib.Path(__file__).resolve().parent / "the_queen_input.txt")
OUTPUT_PATH = str(pathlib.Path(__file__).resolve().parent / "test_output.json")
LOG_PATH = str(pathlib.Path(__file__).resolve().parent / "test.log")


async def worker(ctx: WorkContext, tasks):
    ctx.run("/bin/sh", "-c", "nohup python classifier.py run &")
    async for task in tasks:
        input_path, output_path = task.data
        ctx.send_file(input_path, "/work/input.txt")
        ctx.run("/usr/local/bin/python", "classifier.py", "submit", "/work/input.txt", "/work/output.json")
        ctx.download_file("/work/output.json", output_path)
        yield ctx.commit(timeout=timedelta(minutes=30))
        task.accept_result(result=output_path)


async def run(subnet_tag, driver=None, network=None):
    package = await vm.repo(
        image_hash="c6b743459d3428fb860582e556ceba1c76dbc8a1d599a55dcf73e437",
        min_mem_gib=4.0,
        min_storage_gib=4.0,
    )

    async with Executor(
        package=package,
        max_workers=1,
        budget=10.0,
        timeout=timedelta(minutes=30),
        subnet_tag=subnet_tag,
        driver=driver,
        network=network,
        event_consumer=log_summary(log_event_repr),
    ) as executor:

        async for _ in executor.submit(worker, [Task(data=(INPUT_PATH, OUTPUT_PATH))]):
            print("Task computed")


@click.command()
@click.option("--subnet-tag", default="devnet-beta.1")
@click.option("--driver")
@click.option("--network")
def main(subnet_tag, driver=None, network=None):
    enable_default_logger(
        log_file=LOG_PATH,
        debug_activity_api=True,
        debug_market_api=True,
        debug_payment_api=True,
    )
    loop = asyncio.get_event_loop()
    task = loop.create_task(
        run(subnet_tag=subnet_tag, driver=driver, network=network)
    )

    try:
        loop.run_until_complete(task)
        print("Task computed.")
    except KeyboardInterrupt:
        print("Shutting down...")
        task.cancel()
        try:
            loop.run_until_complete(task)
            print("Done.")
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass

if __name__ == "__main__":
    main()