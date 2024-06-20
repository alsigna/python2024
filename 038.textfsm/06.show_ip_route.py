from pathlib import Path
from pprint import pprint

import textfsm

output = """
R1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      1.0.0.0/32 is subnetted, 1 subnets
C        1.1.1.1 is directly connected, Loopback1
      2.0.0.0/32 is subnetted, 1 subnets
C        2.2.2.2 is directly connected, Loopback2
      10.0.0.0/8 is variably subnetted, 7 subnets, 3 masks
D        10.10.10.0/24 [90/3072] via 192.168.10.1, 00:58:53, GigabitEthernet0/0
O        10.10.20.0/24 [110/3072] via 192.168.20.1, 00:58:53, GigabitEthernet0/1
D        10.10.30.0/24 [90/3072] via 192.168.30.1, 00:58:53, GigabitEthernet0/2
D        10.10.40.0/24 [90/3328] via 192.168.41.1, 00:58:53, GigabitEthernet0/3
                       [90/3328] via 192.168.42.1, 00:58:53, GigabitEthernet0/4

"""


# Value protocol ([DO])
# Value prefix (([\d.]{1,3}){3}\d{1,3}/\d{1,2})
# Value List nhop (([\d.]{1,3}){3}\d{1,3})

# Start
#   ^\w -> Continue.Record
#   ^${protocol}\s+${prefix}.*via\s+${nhop}
#   ^.*via\s+${nhop}


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)
pprint(result)
