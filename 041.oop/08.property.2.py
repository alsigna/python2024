from netaddr import IPAddress


class Switch:
    def __init__(self, ip: str) -> None:
        self.__ip = ip

    @property
    def ip(self) -> str:
        return f"device ip address: {self.__ip}"

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self.__ip = ip


sw = Switch("500.168.1.1")
print(sw.ip)
sw.ip = "192.168.1.2"
print(sw.ip)
sw.ip = "500.1.1.1"
