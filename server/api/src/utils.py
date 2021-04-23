import json


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
    print(f"Yagna started! yagna_account={account}, yagna_app_key={key}")

    return account, key
