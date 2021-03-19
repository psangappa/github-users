import os

from pydantic import BaseSettings
from pydantic import Field


this_filepath = os.path.dirname(os.path.realpath(__file__))
dotenv_path = os.path.join(this_filepath, "../conf/.env")


class Settings(BaseSettings):
    """
    Defines settings for a this Service and their defaults.

    Every option can be also set via environment variable.

    Settings from different sources are merged according to this precedence:
    ENV variables > .env >> model_defaults
    """

    host: str = Field("localhost", description="Bind socket to this host.")
    port: int = Field(8000, description="Bind to a socket with this port.")

    name: str = Field(
        "Github User Service", description="Name of the service."
    )

    class Config:
        env_file = dotenv_path


settings = Settings()
