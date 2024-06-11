from collections import namedtuple
from pprint import pprint
from typing import Generator

output = """
Interface             IP-Address      OK?    Method Status     Protocol
GigabitEthernet0/1    192.168.100.1   YES    unset  up         up
GigabitEthernet0/2    192.168.190.235 YES    unset  up         down
GigabitEthernet0/3    unassigned      YES    unset  up         up
GigabitEthernet0/4    192.168.191.2   YES    unset  up         up
TenGigabitEthernet2/1 unassigned      YES    unset  up         up
TenGigabitEthernet2/2 10.255.1.3      YES    unset  down       down
TenGigabitEthernet2/3 unassigned      YES    unset  up         up
TenGigabitEthernet2/4 unassigned      YES    unset  up         down
GigabitEthernet3/1    unassigned      YES    unset  down       down
GigabitEthernet3/2    unassigned      YES    unset  down       down
GigabitEthernet3/3    unassigned      YES    unset  down       down
GigabitEthernet3/4    unassigned      YES    unset  down       down
Loopback1             unassigned      YES    unset  up         up
Loopback2             10.255.255.100  YES    unset  up         up
""".strip()


Interface = namedtuple("Interface", "name ip ok method status protocol")
interfaces: list[Interface] = []
for line in output.splitlines()[1:]:
    interfaces.append(Interface(*line.split()))


def parse_interface(interfaces: list[Interface]) -> Generator[Interface, None, None]:
    for interface in interfaces:
        match interface:
            case Interface(
                protocol="down",
                ip=str(ip),
                name=str(name),
            ) if ip != "unassigned" and name.startswith("Ten"):
                yield interface

    for interface in interfaces:
        if interface.protocol == "down":
            if (
                isinstance(interface.ip, str)
                and isinstance(interface.name, str)
                and interface.ip != "unassigned"
                and interface.name.startswith("Ten")
            ):
                yield interface


for i in parse_interface(interfaces):
    print(i)
