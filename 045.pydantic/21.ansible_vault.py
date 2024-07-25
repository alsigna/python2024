from typing import Self

from ansible_vault import Vault
from pydantic import model_validator
from pydantic_settings import BaseSettings

# export VAULT_FILE=vault.yaml
# export VAULT_PASSWORD=P@ssw0rd


# vault = Vault("P@ssw0rd")

# data = {
#     "password": "my_secret",
#     "username": "my_name",
# }
# with open("vault.yaml", "w") as f:
#     vault.dump(data, f)


class Settings(BaseSettings):
    class Config:
        extra = "allow"

    vault_password: str
    vault_file: str

    @model_validator(mode="before")
    def init_groups(self) -> Self:
        vault_password = self.get("vault_password")
        vault_file = self.get("vault_file")
        if vault_password is None:
            raise ValueError("Vault Password должен быть задан в ENV")
        if vault_file is None:
            raise ValueError("Vault Filename должен быть задан в ENV")

        vault = Vault(vault_password)
        with open(vault_file, "r") as f:
            enc_data = f.read()
        secret_data = vault.load(enc_data)
        return self | secret_data


settings = Settings()

print(settings)
print(f"{settings.username=}")
print(f"{settings.password=}")
