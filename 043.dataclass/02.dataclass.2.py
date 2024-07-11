from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Interface:
    name: str
    ip: str
    mask: str
    description: str
    status: str = "up"


i = Interface("gi0/1", "192.168.1.1", "255.255.255.0", "to core")
