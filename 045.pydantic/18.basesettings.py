from typing import Literal

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings

# export MY_APP_NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f
# export MY_APP_NB_URL=http://10.211.55.7:8000
# export MY_APP_STAGE=prod


class Settings(BaseSettings):
    nb_url: HttpUrl
    nb_token: SecretStr
    stage: Literal["dev", "stg", "prod"] = "stg"

    class Config:
        case_sensitive = False
        env_prefix = "MY_APP_"


settings = Settings()

print(settings)
