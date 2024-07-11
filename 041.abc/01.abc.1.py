class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def get_running_config(self) -> str:
        raise NotImplementedError("method should be overloaded in nested class")


class CiscoIOS(Device):
    platform = "cisco_ios"


sw = CiscoIOS("192.168.1.1")

config = sw.get_running_config()
print(config)
