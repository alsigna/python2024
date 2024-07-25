from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import auto
from typing import Callable

from strenum import LowercaseStrEnum


class Vendor(LowercaseStrEnum):
    CISCO: str = auto()
    HUAWEI: str = auto()
    ARISTA: str = auto()


class Transport(LowercaseStrEnum):
    SYSTEM: str = auto()
    SSH2: str = auto()
    PARAMIKO: str = auto()
    TELNET: str = auto()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.value.upper()}"

    def __str__(self) -> str:
        return self.value


class Platform(LowercaseStrEnum):
    HUAWEI_VRP: str = auto()
    ARISTA_EOS: str = auto()
    CISCO_IOSXE: str = auto()
    CISCO_NXOS: str = auto()


@dataclass(slots=True, frozen=True)
class Commands:
    running: str
    version: str
    inventory: str


@dataclass(slots=True)
class ABCDevice(ABC):
    hostname: str
    ip: str

    scrapli: dict = field(default_factory=lambda: {"transport": Transport.SYSTEM})

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


@dataclass(repr=False, eq=False)
class CiscoIOS(ABCDevice):
    platform: Platform = Platform.CISCO_IOSXE
    vendor: Vendor = Vendor.CISCO
    commands: Commands = Commands(
        running="show running-config",
        version="show version",
        inventory="show inventory",
    )


@dataclass(repr=False, eq=False)
class HuaweiVRP(ABCDevice):
    platform: Platform = Platform.HUAWEI_VRP
    vendor: Vendor = Vendor.HUAWEI
    commands: Commands = Commands(
        running="display current-configuration",
        version="display version",
        inventory="display device",
    )


@dataclass(repr=False, eq=False)
class AristaEOS(ABCDevice):
    platform: Platform = Platform.ARISTA_EOS
    vendor: Vendor = Vendor.ARISTA
    commands: Commands = Commands(
        running="show running-config",
        version="show version",
        inventory="show inventory",
    )


if __name__ == "__main__":
    uut_classes = {
        CiscoIOS: {
            "platform": Platform.CISCO_IOSXE,
            "vendor": Vendor.CISCO,
            "running": "show running-config",
            "version": "show version",
            "inventory": "show inventory",
        },
        HuaweiVRP: {
            "platform": Platform.HUAWEI_VRP,
            "vendor": Vendor.HUAWEI,
            "running": "display current-configuration",
            "version": "display version",
            "inventory": "display device",
        },
        AristaEOS: {
            "platform": Platform.ARISTA_EOS,
            "vendor": Vendor.ARISTA,
            "running": "show running-config",
            "version": "show version",
            "inventory": "show inventory",
        },
    }
    for c, p in uut_classes.items():
        device = c("r1", "192.168.1.1")
        assert device.platform == p["platform"], f"неправильная платформа для {c.__name__}"
        assert device.vendor == p["vendor"], f"неправильный производитель для {c.__name__}"
        assert device.commands.running == p["running"], f"неправильная running команда для {c.__name__}"
        assert device.commands.version == p["version"], f"неправильная version команда для {c.__name__}"
        assert device.commands.inventory == p["inventory"], f"неправильная inventory команда для {c.__name__}"
        assert str(device) == f"r1/192.168.1.1 ({p['vendor']})", f"неправильный str метод для {c.__name__}"
        other_eq = c("r1", "192.168.1.1")
        other_ne = c("r1", "192.168.1.2")
        assert device == other_eq, f"неправильный eq метод для {c.__name__}"
        assert device != other_ne, f"неправильный eq метод для {c.__name__}"
        assert isinstance(device.__hash__, Callable), f"не определен __hash__ метод для {c.__name__}"
