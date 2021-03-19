from fastapi import FastAPI
import uvicorn
from github_users.api.handlers.users import user_router
from github_users.settings import settings
from github_users import __version__


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
        prefix = "/api/v1"
        self.include_router(user_router, prefix=prefix)


app = UserService(title=settings.name, version=__version__)


def start_api() -> None:
    """Entrypoint for script that starts the API"""
    uvicorn.run(app, host=settings.host, port=settings.port)
