from abc import ABC, abstractmethod
from enum import auto

import settings
from pydantic import AliasPath, BaseModel, Field, field_validator
from strenum import LowercaseStrEnum


class Platform(LowercaseStrEnum):
    CISCO_IOSXE: str = auto()
    ELTEX_ESR: str = auto()
    HUAWEI_VRP: str = auto()


class Vendor(LowercaseStrEnum):
    CISCO: str = auto()
    ELTEX: str = auto()
    HUAWEI: str = auto()


class Commands(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True
        slots = True

    running: str
    version: str
    inventory: str


class Transport(LowercaseStrEnum):
    ASYNCSSH: str = auto()
    ASYNCTELNET: str = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.value.upper()}"

    def __str__(self) -> str:
        return self.value


class NetboxDevice(BaseModel):
    name: str
    platform: str = Field(validation_alias=AliasPath("platform", "slug"))
    ip: str = Field(validation_alias=AliasPath("primary_ip4", "address"))
    vendor: str = Field(validation_alias=AliasPath("device_type", "manufacturer", "slug"))

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        ip, _ = value.split("/")
        return ip

    @field_validator("platform")
    @classmethod
    def map_patform(cls, value: str) -> str:
        NETBOX_SCRAPLI_MAP = {
            "cisco-xe": Platform.CISCO_IOSXE,
            "cisco-ios": Platform.CISCO_IOSXE,
            "huawei-vrp": Platform.HUAWEI_VRP,
            "eltex-esr": Platform.ELTEX_ESR,
        }
        return NETBOX_SCRAPLI_MAP.get(value)


class AppResponse(BaseModel):
    failed: bool
    hostname: str
    output_type: str
    output: str = ""
    msg: str = ""


class ABCDevice(BaseModel, ABC):
    hostname: str
    ip: str

    extra_scrapli: dict = {}

    @property
    @abstractmethod
    def platform(self) -> Platform:
        pass

    @property
    @abstractmethod
    def vendor(self) -> Vendor:
        pass

    @property
    @abstractmethod
    def commands(self) -> Commands:
        pass

    @property
    def scrapli(self) -> dict[str, str]:
        scrapli_template = {
            "transport": Transport.ASYNCTELNET,
            "auth_username": settings.CLI_USERNAME,
            "auth_password": settings.CLI_PASSWORD,
            "auth_secondary": settings.CLI_ENABLE,
            "auth_strict_key": False,
            "ssh_config_file": "./ssh_config",
        }
        return scrapli_template | {"platform": self.platform} | {"host": self.ip} | self.extra_scrapli

    def __str__(self) -> str:
        return f"{self.hostname}/{self.ip} ({self.vendor})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(hostname='{self.hostname}', ip='{self.ip}', scrapli={self.scrapli})"

    def __hash__(self) -> int:
        return hash(self.ip + self.hostname + self.__class__.__name__)

    def __eq__(self, other: object) -> bool:
        return (
            self.ip == other.ip
            and self.hostname == other.hostname
            and self.__class__.__name__ == other.__class__.__name__
        )
