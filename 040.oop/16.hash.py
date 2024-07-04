from __future__ import annotations


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Device) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)


d1 = Device("192.168.1.1", "rt1")
d2 = Device("192.168.1.2", "rt1")

configs = {
    d1: "config1",
    d2: "config2",
}

print(configs)
