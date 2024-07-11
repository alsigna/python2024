from dataclasses import dataclass, field


@dataclass(slots=True)
class Interface:
    name: str
    ip: str
    mask: str
    description: str
    status: str = field(default="up", init=False, repr=False)


i = Interface("gi0/1", "192.168.1.1", "255.255.255.0", "to core")
