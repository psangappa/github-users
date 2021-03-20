from fastapi import FastAPI
import uvicorn
from github_users.api.handlers.users import user_router
from github_users.settings import settings
from github_users import __version__
from github_users.api.async_http_client import SingletonAiohttp
from github_users.core.user_manager import UserManager


class UserService(FastAPI):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setup_app()

    def setup_app(self) -> None:
        """
        Add handlers and managed objects to the environment, before the app
        is started.

        To add managed objects, use

            self.state.my_object = my_object

        To add a handler, use

            self.include_router(my_router)
        """
        self.state.user_manager = UserManager(settings.github_api_url)
        prefix = "/api/v1"
        self.include_router(user_router, prefix=prefix)


app = UserService(title=settings.name, version=__version__)


@app.on_event("startup")
async def on_start_up() -> None:
    """
    A callback method before starting the application.
    Get async http client session.
    """
    SingletonAiohttp.get_aiohttp_client()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """A callback method before shutting down the application."""
    await SingletonAiohttp.close_aiohttp_client()


def start_api() -> None:
    """Entrypoint for script that starts the API"""
    uvicorn.run(app, host=settings.host, port=settings.port)
