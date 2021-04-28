import pytest
import re
from utils import parse_yagna_key

def test_keyfile_is_parsed_correctly():
    keyfile_json = """
{
  "headers": [
    "name",
    "key",
    "id",
    "role",
    "created"
  ],
  "values": [
    [
      "requestor",
      "b242af88911a483da8b46335c15aab4e",
      "0x288bb9f0981ccd96e46781cb90003472a714fc72",
      "manager",
      "2021-04-23T12:26:05.105827690"
    ]
  ]
}
    """

    expected_account, expected_appkey = "0x288bb9f0981ccd96e46781cb90003472a714fc72", "b242af88911a483da8b46335c15aab4e"
    account, appkey = parse_yagna_key(keyfile_json)

    assert expected_account == account
    assert expected_appkey == appkey


def test_invalid_key_legth_fails_on_assert():
    keyfile_json = """
{
  "headers": [
    "name",
    "key",
    "id",
    "role",
    "created"
  ],
  "values": [
    [
      "requestor",
      "too_short_appkey",
      "0x288bb9f0981ccd96e46781cb90003472a714fc72",
      "manager",
      "2021-04-23T12:26:05.105827690"
    ]
  ]
}
    """

    with pytest.raises(AssertionError) as assert_err:
        parse_yagna_key(keyfile_json)

    assert re.search(r"Unable to read Yagna app key.", str(assert_err))
