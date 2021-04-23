from pathlib import Path
from time import sleep, time

import json


def get_yagna_app_key(full_path: str, max_wait_time_seconds: int) -> (str, str):
    print(f"Waiting for Yagna service ready... (allowing {max_wait_time_seconds} secs)")
    full_path = Path(full_path)
    wait_start = time()

    while not full_path.exists():
        sleep(0)
        assert time() - wait_start < max_wait_time_seconds, "Yagna service was not ready in the time period."
    yagna_account, yagna_app_key = parse_yagna_key(full_path.read_text())

    print(f"{yagna_account=}, {yagna_app_key=}")
    return yagna_account, yagna_app_key


def parse_yagna_key(response_json: str) -> (str, str):
    """Parses the yagna app key from the output of `yagna app-key list --json`"""

    key_data = json.loads(response_json)

    name_idx = key_data['headers'].index('name')
    key_idx = key_data['headers'].index('key')
    account_idx = key_data['headers'].index('id')

    acc_data = [(v[account_idx], v[key_idx]) for v in key_data['values'] if v[name_idx] == "requestor"]

    assert len(acc_data) == 1, "Bad app_key file content."
    [(account, key)] = acc_data
    assert len(key) == 32, "Unable to read Yagna app key."
    assert len(account) == 2 + 2 * 20, "Unable to read default requestor account"

    return account, key
