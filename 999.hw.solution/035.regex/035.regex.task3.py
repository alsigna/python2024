import re
from collections import namedtuple
from typing import Generator

output = """
rt# show ip interface brief
Interface             IP-Address      OK?    Method Status                   Protocol
GigabitEthernet0/1    192.168.100.1   YES    unset  up                          up
GigabitEthernet0/2    192.168.190.235 YES    unset  up                          up
GigabitEthernet0/3    unassigned      YES    unset  up                          up
GigabitEthernet0/4    192.168.191.2   YES    unset  up                          up
TenGigabitEthernet2/1 unassigned      YES    unset  up                          up
TenGigabitEthernet2/2 10.255.1.3      YES    unset  up                          up
TenGigabitEthernet2/2.100 10.255.100.3      YES    unset  up                          up
TenGigabitEthernet2/3 unassigned      YES    unset  up                          up
TenGigabitEthernet2/4 unassigned      YES    unset  up                          down
GigabitEthernet3/1    unassigned      YES    unset  administratively down       down
GigabitEthernet3/2    unassigned      YES    unset  down                        down
GigabitEthernet3/3    unassigned      YES    unset  administratively down       down
GigabitEthernet3/4    unassigned      YES    unset  down                        down
Loopback1             unassigned      YES    unset  up                          up
Loopback2             10.255.255.100  YES    unset  administratively down       down
""".strip()

IPInterface = namedtuple("IPInterface", "name status protocol ip")


def parse_show_ip_int_br(output: str, unassigned: bool = True) -> Generator[IPInterface, None, None]:
    if unassigned:
        IP = r"(?P<ip>(?:[\d.]+|unassigned))"
    else:
        IP = r"(?P<ip>[\d.]+)"
    STATUS = r"(?P<status>(?:up|down|administratively down))"
    PROTOCOL = r"(?P<protocol>(?:up|down))"
    NAME = r"(?P<name>[\w/.]+)"
    pattern: re.Pattern = re.compile(rf"{NAME}\s+{IP}\s+YES\s+\w+\s+{STATUS}\s+{PROTOCOL}")
    for line in output.splitlines():
        if (m := pattern.search(line)) is None:
            continue
        yield IPInterface(**m.groupdict())


for interface in parse_show_ip_int_br(output, unassigned=False):
    print(interface)
