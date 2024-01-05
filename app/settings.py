import os
from pydantic_settings import BaseSettings

databasedir = os.getcwd()
databasedir = databasedir[:databasedir.rfind('\\')]
imagesdir = os.path.join(databasedir, "images")


class Settings:
    server_host = "0.0.0.0"
    server_port = 80
    database_url: str | None = "sqlite:///./database.sqlite3"
    ssl_keyfile = None
    ssl_certfile = None


class SettingsDeprecated(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 80
    #database_url: str = f"sqlite:///{databasedir}/database.sqlite3"
    database_url: str | None = "sqlite:///./database.sqlite3",
    ssl_keyfile: str | None = None,
    ssl_certfile: str | None = None


settings = Settings()

