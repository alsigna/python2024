import re
from collections import namedtuple

sw1_output = """
sw1# show switch
                                            H/W   Current
 Switch#  Role   Mac Address     Priority Version  State
 ----------------------------------------------------------
 *1       Master 0018.ba60.de00     15       1     Ready
  2       Member 0018.ba60.ce00     14       1     Ready
  3       Member 0016.9d0c.7500     1        2     Version Mismatch
""".strip()

# [
#     StackMember(id=1, role="Master", mac="0018.ba60.de00", priority=15, revision=1, state="Ready"),
#     StackMember(id=2, role="Member", mac="0018.ba60.ce00", priority=14, revision=1, state="Ready"),
#     StackMember(id=3, role="Member", mac="0016.9d0c.7500", priority=1, revision=2, state="Version Mismatch"),
# ]


sw2_output = """
sw2> show switch
                                               Current
Switch#  Role      Mac Address     Priority     State
--------------------------------------------------------
 1       Slave     0016.4748.dc80     5         Ready
*2       Master    0016.9d59.db00     1         Ready
""".strip()

# [
#     StackMember(id=1, role="Slave", mac="0016.4748.dc80", priority=5, revision=0, state="Ready"),
#     StackMember(id=2, role="Master", mac="0016.9d59.db00", priority=1, revision=0, state="Ready"),
# ]


StackMember = namedtuple("StackMember", "id role mac priority revision state")


def parse_show_switch(output: str) -> list[StackMember]:
    result: list[StackMember] = []

    for switch in re.finditer(
        pattern=r"\s*\*?(?P<id>\d+)\s+(?P<role>\w+)\s+(?P<mac>\S+)\s+(?P<priority>\d+)\s+(?P<revision>\d+)?\s+(?P<state>[\w ]+)",
        string=output,
    ):
        switch_data = switch.groupdict()
        if switch_data.get("revision") is None:
            switch_data["revision"] = 0

        for k, v in switch_data.items():
            if isinstance(v, str) and v.isdigit():
                switch_data[k] = int(v)

        result.append(StackMember(**switch_data))

    return result


if __name__ == "__main__":
    print(parse_show_switch(sw2_output))
