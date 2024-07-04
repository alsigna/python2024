class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        print("Device init")
        self.hostname = hostname
        self.ip = ip

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}")


class Cisco:
    def __init__(self) -> None:
        print("Cisco init")
        self.vendor = "cisco"


class Router(Device, Cisco):
    def __init__(self, hostname: str, ip: str, platform: str) -> None:
        print("Router init")
        super().__init__(hostname, ip)
        self.platform = platform


rt = Router("rt1", "192.168.1.1", "xe")
