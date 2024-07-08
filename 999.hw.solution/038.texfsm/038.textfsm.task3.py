from pathlib import Path
from pprint import pprint

import textfsm

output = """
Router# show ip interface brief
Interface             IP-Address      OK?    Method Status     Protocol
GigabitEthernet0/1    192.168.100.1   YES    unset  up         up
GigabitEthernet0/2    192.168.190.235 YES    unset  up         down
TenGigabitEthernet2/1 unassigned      YES    unset  up         up
TenGigabitEthernet2/2 10.255.1.3      YES    unset  up         up
GigabitEthernet3/1    unassigned      YES    unset  down       down
GigabitEthernet3/2    unassigned      YES    unset  down       down
Loopback1             unassigned      YES    unset  up         up
Loopback2             10.255.255.100  YES    unset  down       down
""".strip()

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)
pprint(result)
