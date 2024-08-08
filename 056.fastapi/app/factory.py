from typing import ClassVar, Type, cast

from models import ABCDevice, Commands, Platform, Vendor

# # @dataclass(repr=False, eq=False)
# class AristaEOS(ABCDevice):
#     platform: Platform = Platform.ARISTA_EOS
#     vendor: Vendor = Vendor.ARISTA
#     commands: Commands = Commands(
#         running="show running-config",
#         version="show version",
#         inventory="show inventory",
#     )


class CiscoIOS(ABCDevice):
    platform: ClassVar[Platform] = Platform.CISCO_IOSXE
    vendor: ClassVar[Vendor] = Vendor.CISCO
    commands: ClassVar[Commands] = Commands(
        running="show running-config",
        version="show version",
        inventory="show inventory",
    )


class HuaweiVRP(ABCDevice):
    platform: ClassVar[Platform] = Platform.HUAWEI_VRP
    vendor: ClassVar[Vendor] = Vendor.HUAWEI
    commands: ClassVar[Commands] = Commands(
        running="display current-configuration",
        version="display version",
        inventory="display device",
    )


class DeviceFactory:
    PLATFORM_MAP = {
        Platform.CISCO_IOSXE: CiscoIOS,
        Platform.HUAWEI_VRP: HuaweiVRP,
    }

    def __new__(cls, platform: Platform, hostname: str, ip: str, extra_scrapli: dict = {}) -> ABCDevice:
        _class: Type[ABCDevice] = cls.get_class(platform)
        device = _class(hostname=hostname, ip=ip, extra_scrapli=extra_scrapli)
        device = cast(ABCDevice, device)
        return device

    @classmethod
    def get_class(cls, platform: str) -> Type[ABCDevice]:
        _class = cls.PLATFORM_MAP.get(platform)
        if _class is None:
            raise NotImplementedError(f"Неизвестная платформа {platform}")
        return _class

    @classmethod
    def create(cls, platform: str, hostname: str, ip: str, extra_scrapli: dict = {}) -> ABCDevice:
        _class = cls.get_class(platform)
        return _class(hostname=hostname, ip=ip, extra_scrapli=extra_scrapli)
