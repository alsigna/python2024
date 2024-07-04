from __future__ import annotations

from typing import Any


class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __eq__(self, other: Device) -> bool:
        return self.ip == other.ip

    def __hash__(self) -> int:
        return hash(self.ip)

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"

    def __contains__(self, value: Any) -> True:
        return value == self.ip


device = Device("192.168.1.2", "rt2")


def check_ip(ip: str) -> None:
    if ip in device:
        print(f"{ip} belongs to `{device}`")
    else:
        print(f"there is no ip {ip} on `{device}`")


for ip in ["192.168.1.2", "192.168.1.200"]:
    check_ip(ip)
