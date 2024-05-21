# display lldp neighbor brief
from pprint import pprint

lldp_output = """
GE1/0/1          br1.hq            GE0/0/5             107
GE1/0/2          br2.hq            GE0/0/5             92
GE1/0/3          sw1.hq            GE1/0/47            98
XGE1/0/1         sw2.hq            GE1/0/51            93
GE2/0/2          br2.hq            GE0/0/6             112
GE2/0/3          sw12.hq           GE1/0/48            98
XGE2/0/1         sw2.hq            GE1/0/52            93
""".strip()

# display interface description
description_output = """
GigabitEthernet1/0/1        up      up       br1.hq.net.ru
GigabitEthernet1/0/2        up      up       br2.hq.net.ru
GigabitEthernet1/0/3        up      up       sw1.hq.net.ru
GigabitEthernet2/0/1        up      up       br1.hq.net.ru
GigabitEthernet2/0/2        up      up       br2.hq.net.ru
GigabitEthernet2/0/3        up      up       sw1.hq.net.ru
XGigabitEthernet1/0/1       up      up       sw2.hq.net.ru
XGigabitEthernet2/0/1       up      up       sw2.hq.net.ru
""".strip()

lldp_dict = {}
descr_dict = {}
if_name_format_rules = {
    "GE": "GigabitEthernet",
    "XGE": "XGigabitEthernet",
}
domain_format_rules = {
    ".net.ru": "",
}

for line in lldp_output.splitlines():
    if_name, peer, *_ = line.split()
    for rule, pattern in if_name_format_rules.items():
        if if_name.startswith(rule):
            if_name = if_name.replace(rule, pattern)
    lldp_dict[if_name] = peer

for line in description_output.splitlines():
    if_name, *_, peer = line.split()
    for rule, pattern in domain_format_rules.items():
        if peer.endswith(rule):
            peer = peer.replace(rule, pattern)
    descr_dict[if_name] = peer


for if_name, lldp_peer in lldp_dict.items():
    if if_name not in descr_dict:
        print(f"интерфейс {if_name} есть в lldp, но нет в description")
        continue
    descr_peer = descr_dict.get(if_name)
    if descr_peer != lldp_peer:
        print(f"lldp сосед {lldp_peer} отличается от description {descr_peer} на интерфейсе {if_name}")

for if_name, descr_peer in descr_dict.items():
    if if_name not in lldp_dict:
        print(f"интерфейс {if_name} есть в description, но нет в lldp")
