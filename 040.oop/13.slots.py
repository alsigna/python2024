class Device:
    __slots__ = ["ip", "hostname"]

    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname


d = Device("192.168.1.1", "rt1")

d.location = "msk"
