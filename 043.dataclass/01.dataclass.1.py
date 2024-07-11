from collections import namedtuple
from dataclasses import dataclass

InterfaceNT = namedtuple("IPInterfaceNT", "name ip mask description status")
intf1 = InterfaceNT("gi0/1", "192.168.1.1", "255.255.255.0", "to core", "up")


@dataclass
class InterfaceDC:
    name: str
    ip: str
    mask: str
    description: str
    status: str


intf2 = InterfaceDC("gi0/1", "192.168.1.1", "255.255.255.0", "to core", "up")
