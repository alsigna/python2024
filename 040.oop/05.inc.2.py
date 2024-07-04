from netaddr import IPAddress


class Device:
    def __init__(self) -> None:
        self.__ip = "0.0.0.0"

    def ip(self) -> str:
        return self.__ip

    def set_ip(self, ip: str) -> None:
        _ = IPAddress(ip)
        self.__ip = ip


d = Device()

print(d.ip())
d.set_ip("192.168.1.1")
print(d.ip())

d.set_ip("wrong string")
