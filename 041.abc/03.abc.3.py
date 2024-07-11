from abc import ABC, abstractmethod
from typing import Any, Self, cast


class AbstactDevice(ABC):
    @property
    @abstractmethod
    def platform(self) -> str: ...

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def get_running_config(self) -> str: ...


class CiscoIOS(AbstactDevice):
    platform = "cisco_ios"

    def get_running_config(self) -> str:
        return "cisco ios config"


class HuaweiVRP(AbstactDevice):
    platform = "huawei_vrp"

    def get_running_config(self) -> str:
        return "huawei vrp config"


class DeviceFactory:
    PLATFORM_MAP = {
        "cisco_ios": CiscoIOS,
        "huawei_vrp": HuaweiVRP,
    }

    @classmethod
    def create(cls, platform: str, *args, **kwargs) -> AbstactDevice:
        _device_class = cls.PLATFORM_MAP.get(platform)
        if _device_class is None:
            raise NotImplementedError("unknown platform")

        return _device_class(*args, **kwargs)


r1 = DeviceFactory.create("cisco_ios", "192.168.1.1")
r2 = DeviceFactory.create("huawei_vrp", "192.168.1.2")

print(r1.get_running_config())
print(r2.get_running_config())


class Device:
    PLATFORM_MAP = {
        "cisco_ios": CiscoIOS,
        "huawei_vrp": HuaweiVRP,
    }

    def __new__(cls, platform: str, *args, **kwargs) -> AbstactDevice:
        _device_class = cls.PLATFORM_MAP.get(platform)
        if _device_class is None:
            raise NotImplementedError("unknown platform")

        return _device_class(*args, **kwargs)


r3 = Device("cisco_ios", "192.168.1.1")
r4 = Device("huawei_vrp", "192.168.1.2")

print(r3.get_running_config())
print(r3.ip)
print(r4.get_running_config())
print(r4.ip)
