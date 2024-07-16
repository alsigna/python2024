from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: HttpUrl
    token: str

    class Config:
        env_file = "./.env"


settings = Settings()

print(settings)
