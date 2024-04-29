from typing import Any
import aiohttp
from packaging.version import Version
import asyncio
from .errors import error_map, PulseError
from .types import ClassifyPayload, ClassifyResponse


class Pulse:
    http: aiohttp.ClientSession
    site_key: str
    secret_key: str

    def __init__(self, site_key: str, secret_key: str):
        self.site_key = site_key
        self.secret_key = secret_key
        loop = None

        if Version(aiohttp.__version__) < Version("4.0.0"):
            loop = asyncio.get_event_loop()

        self.http = aiohttp.ClientSession(
            loop=loop,
            headers={
                "content-type": "application/json",
            },
            raise_for_status=False,
            base_url="https://api.pulsesecurity.org",
        )

    async def close(self):
        await self.http.close()

    async def classify(self, token: str, **kwargs: Any) -> bool:
        """Classify a token to check if it's a bot or not.

        Parameters
        ----------
        token : str
            The token to classify.
        timeout : int, optional
            The request timeout in seconds. Default is 10.

        Returns
        -------
        bool
            Whether the token is a bot or not.
        """

        payload = ClassifyPayload(
            token=token, site_key=self.site_key, secret_key=self.secret_key
        )

        timeout = kwargs.get("timeout", 10)

        async with self.http.post(
            "/api/classify", json=payload, timeout=timeout
        ) as resp:
            data = await resp.json()
            response = ClassifyResponse.from_dict(data)

            if response.errors:
                error = response.errors[0]
                cls = error_map.get(error.code, PulseError)
                raise cls(error)

            if response.is_bot is None:
                raise ValueError("is_bot is not present in response")

            return response.is_bot
