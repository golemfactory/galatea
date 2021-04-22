import json


def parse_yagna_key(key_js):
    """Parses the yagna app key from the output of `yagna app-key list --json`"""

    key_data = json.loads(key_js)

    name_idx = key_data['headers'].index('name')
    key_idx = key_data['headers'].index('key')

    key = [v[key_idx] for v in key_data['values'] if v[name_idx] == "requestor"]

    assert len(key) == 1, "Bad app_key file content."
    assert len(key[0]) == 32, "Unable to read Yagna app key."

    return key[0]
