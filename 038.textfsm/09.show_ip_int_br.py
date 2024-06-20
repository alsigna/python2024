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
GigabitEthernet5/1     10.255.255.102  YES NVRAM  up                    up      
"""

# Value interface ([\w./]+)
# Value ip ((\d{1,3}\.){3}\d{1,3})
# Value status (up|down|administratively down)
# Value protocol (up|down)

# Start
#   # junk lines
#   ^$$
#   ^\w+[#>]
#   ^Interface\s+IP-Address\s+
#   ^\S+\s+unassigned\s+
#   # payload
#   ^${interface}\s+${ip}\s+\w+\s+\w+\s+${status}\s+${protocol} -> Record
#   # check for comlience
#   ^.* -> Error "no rule for line"

template = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")
with open(template, "r") as f:
    fsm = textfsm.TextFSM(f)

result = fsm.ParseText(output)

pprint(result)
