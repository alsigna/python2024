from netaddr import IPAddress


class Switch:
    def __init__(self, ip: str, hostname: str) -> None:
        self.__ip = ip
        self.__hostname = hostname

    @property
    def ip(self) -> str:
        return f"device ip address: {self.__ip}"

    @ip.setter
    def ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self.__ip = ip

    def set_hostname(self, hostname: str) -> None:
        self.__hostname = hostname

    def get_hostname(self) -> str:
        return self.__hostname

    hostname = property(get_hostname, set_hostname)


# sw = Switch("500.168.1.1")
# print(sw.ip)
# sw.ip = "192.168.1.2"
# print(sw.ip)
# sw.ip = "500.1.1.1"

sw = Switch("100.168.1.1", "sw1")
