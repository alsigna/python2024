import logging
import re
from typing import Any, ClassVar

from exceptions import FactoryError
from models import ABCDevice, Commands, ScrapliPlatform, ScrapliTransport, Vendor
from scrapli.response import Response

log = logging.getLogger("uvicorn")


class CiscoXE(ABCDevice):
    platform: ClassVar[ScrapliPlatform] = ScrapliPlatform.CISCO_IOSXE
    vendor: ClassVar[Vendor] = Vendor.CISCO
    commands: ClassVar[Commands] = Commands(
        running="show running-config",
        version="show version",
        inventory="show inventory",
    )
    custom_scrapli: dict[str, str] = {"transport": ScrapliTransport.ASYNCSSH}

    def parse_version(self, output: Response) -> str:
        try:
            return output.textfsm_parse_output()[0].get("version")
        except Exception:
            return output.result


class HuaweiVRP(ABCDevice):
    platform: ClassVar[ScrapliPlatform] = ScrapliPlatform.HUAWEI_VRP
    vendor: ClassVar[Vendor] = Vendor.HUAWEI
    commands: ClassVar[Commands] = Commands(
        running="display current-configuration",
        version="display version",
        inventory="display device",
    )

    def parse_version(self, output: Response) -> str:
        if m := re.search(r"Software,\s+Version\s+(?P<version>\S+)\s+", output.result):
            return m.group("version")
        else:
            output.result


class EltexESR(ABCDevice):
    platform: ClassVar[ScrapliPlatform] = ScrapliPlatform.ELTEX_ESR
    vendor: ClassVar[Vendor] = Vendor.ELTEX
    commands: ClassVar[Commands] = Commands(
        running="show running-config",
        version="show version",
        inventory="show system",
    )

    def parse_version(self, output: Response) -> str:
        return output.result


class Device:
    PLATFORM_MAP = {
        "cisco-ios": CiscoXE,
        "cisco-xe": CiscoXE,
        "huawei-vrp": HuaweiVRP,
        "eltex-esr": EltexESR,
    }

    def __new__(cls, platform: str, hostname: str, ip: str, **kwargs: dict[Any, Any]) -> ABCDevice:
        _class: ABCDevice | None = cls.PLATFORM_MAP.get(platform)
        if _class is None:
            raise FactoryError(f"неизвестный тип платформы {platform}")
        log.debug(f"для устройства {hostname} выбран класс {_class.__name__}")
        device = _class(hostname=hostname, ip=ip)
        return device
