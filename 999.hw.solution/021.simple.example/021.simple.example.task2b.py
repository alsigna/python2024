from collections import namedtuple
from pprint import pprint

# display lldp neighbor brief
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


def get_dict_diff(a: dict, b: dict):
    diff = namedtuple("Action", ("added", "removed", "changed", "unchanged"))

    def added():
        # что добавлено в a по сравнению с b
        keys = set(a.keys()) - set(b.keys())
        return {key: a.get(key) for key in keys}

    def removed():
        # что удалено в a по сравнению с b
        keys = set(b.keys()) - set(a.keys())
        return {key: b.get(key) for key in keys}

    def changed():
        # что изменено в a по сравнению с b
        return {key: value for key, value in a.items() if b.get(key) != value}

    def unchanged():
        # совпадения a и b
        return {key: value for key, value in a.items() if b.get(key) == value}

    return diff(added, removed, changed, unchanged)


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

diff = get_dict_diff(lldp_dict, descr_dict)

print("-" * 10, "added", "-" * 10)
pprint(diff.added())

print("-" * 10, "removed", "-" * 10)
pprint(diff.removed())

print("-" * 10, "changed", "-" * 10)
pprint(diff.changed())

print("-" * 10, "unchanged", "-" * 10)
pprint(diff.unchanged())
