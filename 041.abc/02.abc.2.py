from abc import ABC, abstractmethod


class Device(ABC):
    @property
    @abstractmethod
    def platform(self) -> str: ...

    def __init__(self, ip: str) -> None:
        self.ip = ip

    @abstractmethod
    def get_running_config(self) -> str: ...


class CiscoIOS(Device):
    platform = "cisco_ios"

    def get_running_config(self) -> str:
        return "cisco ios config"


sw = CiscoIOS("192.168.1.1")
print(sw.get_running_config())
