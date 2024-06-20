from pathlib import Path
from pprint import pprint

import textfsm

output = "GigabitEthernet1       192.168.122.101 YES NVRAM  down                    up"


# Value interface (\S+)
# Value ip (\S+)
# Value ip2 (((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})
# Value status (up|down|administratively down)
# Value protocol (up|down)

# Start
#   ^${interface}\s+${ip}\s+\w+\s+\w+\s+${status}\s+${protocol}

template = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")
with open(template, "r") as f:
    fsm = textfsm.TextFSM(f)

result = fsm.ParseText(output)
# result = fsm.ParseTextToDicts(output)

# pprint(fsm.header)
pprint(result)
