from pathlib import Path
from pprint import pprint

import tabulate
import textfsm

output = """
sw1# sh etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      f - Giiled to allocate aggregator

        M - not in use, minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - deGiult port


Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP
2      Po2(SU)         LACP      Gi0/21(P) Gi0/22(P) Gi0/23(P) Gi0/24(P)
                                 Gi0/25(P) Gi0/26(P) Gi0/27(P) Gi0/28(P)
                                 Gi0/29(P)
3      Po3(SU)         LACP      Gi0/31(P) Gi0/32(P) Gi0/33(P)
4      Po4(SU)         LACP      Gi0/41(P)

"""

# Value po_name (\S+)
# Value po_status (\D+)
# Value protocol (-|LACP|PAgP)
# Value List members ([\w./]+)

# Start
#   ^\d+\s+ -> Continue.Record
#   ^\d+\s+${po_name}\(${po_status}\)\s+${protocol}\s? -> Continue
#   ^.*(-|LACP|PAgP)\s*$$
#   ^.*(-|LACP|PAgP)\s+([\w./]+\(\w+\)\s+){0}${members}\(\w+\) -> Continue
#   ^.*(-|LACP|PAgP)\s+([\w./]+\(\w+\)\s+){1}${members}\(\w+\) -> Continue
#   ^.*(-|LACP|PAgP)\s+([\w./]+\(\w+\)\s+){2}${members}\(\w+\) -> Continue
#   ^.*(-|LACP|PAgP)\s+([\w./]+\(\w+\)\s+){3}${members}\(\w+\) -> Continue
#   ^\s+([\w./]+\(\w+\)\s+){0}${members}\(\w+\) -> Continue
#   ^\s+([\w./]+\(\w+\)\s+){1}${members}\(\w+\) -> Continue
#   ^\s+([\w./]+\(\w+\)\s+){2}${members}\(\w+\) -> Continue
#   ^\s+([\w./]+\(\w+\)\s+){3}${members}\(\w+\) -> Continue


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as f:
    fsm = textfsm.TextFSM(f)

result = fsm.ParseTextToDicts(output)
pprint(result)
# print(tabulate.tabulate(result, fsm.header))
