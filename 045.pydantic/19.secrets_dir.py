from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: HttpUrl
    token: str

    class Config:
        secrets_dir = "./secrets/"


settings = Settings()

print(settings)

print(f"{str(settings.url)=}")
print(f"{settings.token=}")
