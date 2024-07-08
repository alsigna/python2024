from pathlib import Path
from pprint import pprint

import textfsm

output = """
sw1# show switch
                                            H/W   Current
 Switch#  Role   Mac Address     Priority Version  State
 ----------------------------------------------------------
 *1       Master 0018.ba60.de00     15       1     Ready
  2       Member 0018.ba60.ce00     14       1     Ready
  3       Member 0016.9d0c.7500     1        2     Version Mismatch
""".strip()

output1 = """
sw2> show switch
                                               Current
Switch#  Role      Mac Address     Priority     State
--------------------------------------------------------
 1       Slave     0016.4748.dc80     5         Ready
*2       Master    0016.9d59.db00     1         Ready
""".strip()


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)
pprint(result)
