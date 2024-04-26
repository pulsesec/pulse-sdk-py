import dataclasses
import json
import pytest
import pulse
from pulse.types import ClassifyResponse, APIResponse, APIErrorData

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
async def test_classify_human(mocker):
    res = MockResponse(ClassifyResponse(is_bot=False, errors=None), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=res)

    client = pulse.PulseAPI(test_site_key, test_secret_key)

    is_bot = await client.classify(test_token)
    assert is_bot is False

    await client.close()


@pytest.mark.asyncio
async def test_classify_bot(mocker):
    res = MockResponse(ClassifyResponse(is_bot=True, errors=None), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=res)

    client = pulse.PulseAPI(test_site_key, test_secret_key)

    is_bot = await client.classify(test_token)
    assert is_bot is True

    await client.close()


@pytest.mark.asyncio
async def test_error_token_not_found(mocker):
    error = APIErrorData(code="TOKEN_NOT_FOUND", error="Token not found")
    res = MockResponse(APIResponse(errors=[error]), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=res)

    client = pulse.PulseAPI(test_site_key, test_secret_key)

    try:
        await client.classify(test_token)
        assert False
    except pulse.TokenNotFoundError as e:
        assert e.code == error.code

    await client.close()


@pytest.mark.asyncio
async def test_error_token_used(mocker):
    error = APIErrorData(code="TOKEN_USED", error="Token used")
    res = MockResponse(APIResponse(errors=[error]), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=res)

    client = pulse.PulseAPI(test_site_key, test_secret_key)

    try:
        await client.classify(test_token)
        assert False
    except pulse.TokenUsedError as e:
        assert e.code == error.code

    await client.close()
