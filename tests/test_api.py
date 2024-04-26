import dataclasses
import json
import pytest
import pulse
from pulse.types import ClassifyResponse, APIResponse, APIErrorData
from typing import List, Tuple, Type

test_site_key = "siteKey"
test_secret_key = "secretKey"
test_token = "token"


class MockResponse:
    def __init__(self, data, status):
        self.data = json.dumps(dataclasses.asdict(data))
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def json(self):
        return json.loads(self.data)


@pytest.mark.asyncio
async def test_classify_bot(mocker):
    res = MockResponse(ClassifyResponse(is_bot=True, errors=None), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=res)

    client = pulse.PulseAPI(test_site_key, test_secret_key)

    is_bot = await client.classify(test_token)
    assert is_bot is True

    await client.close()


@pytest.mark.asyncio
async def test_errors(mocker):
    tests: List[Tuple[str, Type[pulse.APIError]]] = [
        ("TOKEN_NOT_FOUND", pulse.TokenNotFoundError),
        ("TOKEN_USED", pulse.TokenUsedError),
        ("TOKEN_EXPIRED", pulse.TokenExpiredError),
    ]

    for code, error in tests:
        res = MockResponse(
            APIResponse(errors=[APIErrorData(code=code, error="Test Error")]), 200
        )
        mocker.patch("aiohttp.ClientSession.post", return_value=res)

        client = pulse.PulseAPI(test_site_key, test_secret_key)

        caught = False

        try:
            await client.classify(test_token)
            assert False
        except error as e:
            assert e.code == code
            caught = True

        assert caught

    await client.close()
