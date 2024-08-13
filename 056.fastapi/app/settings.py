from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    APP_NAME: str = "device-walker"

    NETBOX_URL: HttpUrl
    NETBOX_TOKEN: str

    CLI_USERNAME: str
    CLI_PASSWORD: str
    CLI_ENABLE: str


settings = Settings()
