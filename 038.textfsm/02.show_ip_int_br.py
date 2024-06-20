from pathlib import Path
from pprint import pprint

import textfsm

output = """
r1#sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.122.101 YES NVRAM  up                    up      
GigabitEthernet2       192.168.12.1    YES NVRAM  up                    up      
GigabitEthernet3       unassigned      YES NVRAM  administratively down down    
GigabitEthernet4       unassigned      YES NVRAM  administratively down down    
Loopback0              10.255.255.101  YES NVRAM  up                    up      
"""

# Value interface (\S+)
# Value ip (\S+)
# Value ip2 (((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})
# Value status (up|down|administratively down)
# Value protocol (up|down)

# Start
#   ^${interface}\s+${ip}\s+\w+\s+\w+\s+${status}\s+${protocol} -> Record

template = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")
with open(template, "r") as f:
    fsm = textfsm.TextFSM(f)

result = fsm.ParseText(output)
# result = fsm.ParseTextToDicts(cli_output)

pprint(fsm.header)
pprint(result)
