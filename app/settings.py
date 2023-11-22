from functools import cache
from os import getenv

from pydantic import IPvAnyAddress, PostgresDsn
from pydantic_settings import BaseSettings

is_dbg = getenv("APP_DEBUG", False) == "True"


class Settings(BaseSettings):
    DEBUG: bool = is_dbg

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn

    # pydantic will fail from the extra env vars
    APP_DEBUG: bool = is_dbg
    FAKE_DB: bool = False
    PGADMIN_DEFAULT_EMAIL: str = ""
    PGADMIN_DEFAULT_PASSWORD: str = ""
    PGADMIN_DISABLE_POSTFIX: bool = True
    PGADMIN_CONFIG_SERVER_MODE: bool = False
    PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: bool = False

    HOST: IPvAnyAddress
    PORT: int
    JSON_LOGS: bool = False
    RELOAD: bool = True if is_dbg else False

    class Config:
        env_file = "./.devenv"  # if is_dbg else "./.env"


@cache
def get_settings():
    return Settings()


settings = get_settings()
