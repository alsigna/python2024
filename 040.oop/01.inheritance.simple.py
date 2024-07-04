class Device:
    def __init__(self, hostname: str, ip: str) -> None:
        self.hostname = hostname
        self.ip = ip

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}")


class Switch(Device):
    def add_vlan(self, vlan_id: int) -> None:
        print(f"adding vlan {vlan_id}")


class Router(Device):
    def __init__(self, hostname: str, ip: str, platform: str) -> None:
        super().__init__(hostname, ip)
        self.platform = platform

    def show_info(self) -> None:
        print(f"{self.hostname=}, {self.ip=}, {self.platform=}")


sw = Switch("rt1", "192.168.1.1")
rt = Router("rt1", "192.168.1.1", "xe")

sw.show_info()
rt.show_info()
