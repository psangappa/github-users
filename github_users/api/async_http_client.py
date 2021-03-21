"""A Custom aiohttp http client"""

import aiohttp
import logging
from typing import Optional
from typing import Any
from github_users.settings import settings


logger = logging.getLogger(__name__)


class AuthorizationError(Exception):
    """Authorization error when wrong/empty access token is provided."""
    pass


class SingletonAiohttp:
    """
    A singleton class.
    Opens client session at application startup.
    Closes client session at application shutdown.
    """

    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            cls.aiohttp_client = aiohttp.ClientSession()

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def get(cls, url: str) -> Any:
        """
        Authenticate with GitHub API with a Personal access token.
        """
        client = cls.get_aiohttp_client()
        async with client.get(
            url,
            headers={
                "accept": "application/vnd.github.v3+json",
                "User-Agent": settings.name,
                "Authorization": f"token {settings.github_token}",
            },
        ) as response:
            if response.status == 401:
                raise AuthorizationError()
            if response.status == 404:
                logger.error(f"The resource at url `{url}` is not found")
                return {}
            if response.status == 409:
                logger.error(f"Git Repository at `{url}` is empty.")
                return {}
            if response.status != 200:
                raise Exception(
                    f"Error when talking to Github: {str(await response.text())}"
                )

            json_result = await response.json()
        return json_result
