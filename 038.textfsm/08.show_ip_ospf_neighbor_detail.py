from pathlib import Path
from pprint import pprint

import textfsm

output = """
 Neighbor 10.255.255.103, interface address 192.168.23.2
    In the area 0 via interface GigabitEthernet0/2
    Neighbor priority is 0, State is FULL, 6 state changes
    DR is 0.0.0.0 BDR is 0.0.0.0
    Options is 0x12 in Hello (E-bit, L-bit)
    Options is 0x52 in DBD (E-bit, L-bit, O-bit)
    LLS Options is 0x1 (LR)
    Dead timer due in 00:00:39
    Neighbor is up for 00:29:12
    Index 1/2/2, retransmission queue length 0, number of retransmission 0
    First 0x0(0)/0x0(0)/0x0(0) Next 0x0(0)/0x0(0)/0x0(0)
    Last retransmission scan length is 0, maximum is 0
    Last retransmission scan time is 0 msec, maximum is 0 msec
 Neighbor 10.255.255.101, interface address 192.168.12.1
    In the area 0 via interface GigabitEthernet0/1
    Neighbor priority is 0, State is FULL, 6 state changes
    DR is 0.0.0.0 BDR is 0.0.0.0
    Options is 0x12 in Hello (E-bit, L-bit)
    Options is 0x52 in DBD (E-bit, L-bit, O-bit)
    LLS Options is 0x1 (LR)
    Dead timer due in 00:00:35
    Neighbor is up for 00:34:35
    Index 1/1/1, retransmission queue length 0, number of retransmission 0
    First 0x0(0)/0x0(0)/0x0(0) Next 0x0(0)/0x0(0)/0x0(0)
    Last retransmission scan length is 0, maximum is 0
    Last retransmission scan time is 0 msec, maximum is 0 msec
"""

# Value Required neighbor_id (\d+\.\d+\.\d+\.\d+)
# Value Required local_ip (\d+\.\d+\.\d+\.\d+)
# Value area (\d+)
# Value local_interface (\S+)
# Value state (\S+)

# Start
#   ^\s*Neighbor\s+${neighbor_id},\s+interface\s+address\s+${local_ip} -> Neighbor

# Neighbor
#   ^\s+In\s+the\s+area\s+${area}\s+via\s+interface\s+${local_interface}
#   ^\s+Neighbor\s+priority\s+is\s\d+,\s+State\s+is\s+${state},
#   ^\s+Last\s+retransmission\s+scan\s+time -> Record Start

template = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)

pprint(result)
