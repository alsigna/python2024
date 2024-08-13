from abc import ABC, abstractmethod
from enum import auto
from typing import ClassVar

import settings
from pydantic import AliasPath, BaseModel, Field, field_validator
from strenum import LowercaseStrEnum


class Vendor(LowercaseStrEnum):
    HUAWEI = auto()  # huawei
    CISCO = auto()  # cisco
    ELTEX = auto()


class ScrapliPlatform(LowercaseStrEnum):
    CISCO_IOSXE = auto()
    HUAWEI_VRP = auto()
    ELTEX_ESR = auto()


class ScrapliTransport(LowercaseStrEnum):
    ASYNCSSH = auto()
    ASYNCTELNET = auto()


class CommandType(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True
        slots = True

    running: str
    version: str
    inventory: str
    save: str


class DeviceWalkerResponse(BaseModel):
    hostname: str
    failed: bool
    output: str = ""
    msg: str = ""


class NetboxDevice(BaseModel):
    name: str
    vendor: str = Field(validation_alias=AliasPath("device_type", "manufacturer", "slug"))
    platform: str = Field(validation_alias=AliasPath("platform", "slug"))
    ip: str = Field(validation_alias=AliasPath("primary_ip", "address"))

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        ip, _ = value.split("/")
        return ip


device = {
    "host": "1.2.3.4",
    "platform": "cisco_iosxe",
    "platform": "huawei_vrp",
    "platform": "eltex_esr",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": "./ssh_config",
}


class ABCDevice(BaseModel, ABC):
    hostname: str
    ip: str
    # extra_scrapli: dict = {}

    @property
    @abstractmethod
    def platform(self) -> ScrapliPlatform:
        pass

    @property
    @abstractmethod
    def vendor(self) -> Vendor:
        pass

    @property
    @abstractmethod
    def commands(self) -> CommandType:
        pass

    @property
    def scrapli(self) -> dict[str, str]:
        scrapli_template = {
            "transport": ScrapliTransport.ASYNCTELNET,
            "auth_username": settings.CLI_USERNAME,
            "auth_password": settings.CLI_PASSWORD,
            "auth_secondary": settings.CLI_ENABLE,
            "auth_strict_key": False,
            "ssh_config_file": "./ssh_config",
        }
        return scrapli_template | {"platform": self.platform} | {"host": self.ip}

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


class CiscoXE(ABCDevice):
    platform: ClassVar[ScrapliPlatform] = ScrapliPlatform.CISCO_IOSXE
    vendor: ClassVar[Vendor] = Vendor.CISCO
    commands: ClassVar[CommandType] = CommandType(
        running="show running-config",
        version="show version",
        inventory="show inventory",
        save="write memory",
    )


class HuaweiVRP(ABCDevice):
    platform: ClassVar[ScrapliPlatform] = ScrapliPlatform.HUAWEI_VRP
    vendor: ClassVar[Vendor] = Vendor.HUAWEI
    commands: ClassVar[CommandType] = CommandType(
        running="display current-configuration",
        version="display version",
        inventory="display device",
        save="save",
    )
