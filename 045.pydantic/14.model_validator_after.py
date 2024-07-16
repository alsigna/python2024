import os
from ipaddress import IPv4Address
from typing import Self

import requests
from pydantic import AliasPath, BaseModel, Field, field_validator, model_validator
from pydantic_extra_types.mac_address import MacAddress


def get_nb_device(hostname: str) -> dict[str, str]:
    # export NB_URL=http://10.211.55.7:8000
    # export NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f

    url = os.environ.get("NB_URL", "")
    token = os.environ.get("NB_TOKEN", "")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(
        url=f"{url}/api/dcim/devices/?name={hostname}",
        headers=headers,
    )
    response.raise_for_status()
    result_json = response.json()
    if result_json["count"] != 1:
        return {}
    else:
        return result_json["results"][0]


def get_nb_interfaces(hostname: str) -> list[dict[str, str]]:
    # export NB_URL=http://10.211.55.7:8000
    # export NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f

    url = os.environ.get("NB_URL", "")
    token = os.environ.get("NB_TOKEN", "")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(
        url=f"{url}/api/dcim/interfaces/?device={hostname}",
        headers=headers,
    )
    response.raise_for_status()
    result_json = response.json()
    if result_json["count"] == 0:
        return []
    else:
        return result_json["results"]


class IP(BaseModel):
    address: IPv4Address
    mask: int = Field(ge=0, le=32)


class Site(BaseModel):
    name: str
    description: str


class Interface(BaseModel):
    name: str
    type: str = Field(validation_alias=AliasPath("type", "value"))
    mtu: int = 1500
    mac: MacAddress | None = Field(alias="mac_address", default=None)

    @model_validator(mode="after")
    def check_mac_address_is_set(self) -> Self:
        if self.name.lower().startswith("gi") and self.mac is None:
            # raise ValueError(f"Для интерфейса {self.name} не установлен MAC")
            self.mac = "00:00:00:00:00:00"
        return self


class Device(BaseModel):
    name: str
    model: str = Field(validation_alias=AliasPath("device_type", "model"))
    vendor: str = Field(validation_alias=AliasPath("device_type", "manufacturer", "name"))
    role: str = Field(validation_alias=AliasPath("role", "name"))
    serial: str
    site: Site
    mgmt_ip: IP = Field(validation_alias=AliasPath("primary_ip4", "address"))
    interfaces: list[Interface] = []

    @field_validator("vendor")
    @classmethod
    def validate_vendor(cls, value: str) -> str:
        if value.lower() not in ["huawei", "cisco", "arista"]:
            raise ValueError(f"неизвестный проиводитель {value}")
        return value.upper()

    @field_validator("mgmt_ip", mode="before")
    @classmethod
    def validate_ip(cls, value: str) -> dict[str, str]:
        address, mask = value.split("/")
        return dict(address=address, mask=mask)


hostname = "rt01"
raw_device = get_nb_device(hostname)
raw_interfaces = get_nb_interfaces(hostname)
raw_device["interfaces"] = raw_interfaces
device = Device.model_validate(raw_device)
