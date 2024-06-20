from pathlib import Path

import tabulate
import textfsm

output = """
r2#sh cdp ne
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, 
                  D - Remote, C - CVTA, M - Two-port Mac Relay 

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
r3               Gig 0/2           168              R B             Gig 0/1
r3               Gig 0/0           163              R B             Gig 0/0
r1               Gig 0/1           158              R I   CSR1000V  Gig 2
r1               Gig 0/0           158              R I   CSR1000V  Gig 1
"""

# Value Filldown local_device (\S+)
# Value Required peer_device (\S+)
# Value local_interface (\S+\s\d+(\/\d+)?)
# Value peer_platform ([\S ]+)
# Value peer_interface (\S+\s\d+(\/\d+)?)

# Start
#   ^${local_device}[>#]
#   # r3               Gig 0/2           168              R B             Gig 0/1
#   ^${peer_device}\s+${local_interface}\s+\d+\s+(\S\s)+\s+${peer_platform}\s+${peer_interface}$$ -> Record


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseText(output)

print(tabulate.tabulate(result, fsm.header))
