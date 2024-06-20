from pathlib import Path
from pprint import pprint

import textfsm

output = """
R1#show ip route
D        10.10.10.0/24 [90/3328] via 10.10.20.2, 00:58:53, GigabitEthernet0/1
                       [90/3328] via 10.10.30.2, 00:58:53, GigabitEthernet0/0
"""

# Value protocol ([DO])
# Value prefix (([\d.]{1,3}){3}\d{1,3}/\d{1,2})
# Value List nhop (([\d.]{1,3}){3}\d{1,3})

# Start
#   ^${protocol}\s+${prefix}.*via\s+${nhop}
#   ^.*via\s+${nhop}


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)
pprint(result)
