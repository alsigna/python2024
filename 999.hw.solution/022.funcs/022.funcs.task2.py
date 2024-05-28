interfaces = [
    "Eth0/0",
    "Gig0/4/3",
    "GE4/4",
    "Po3",
    "Ten5/4",
    "XGE4/1",
    "Eth-Trunk4",
    "VLAN10",
]


def normalize_if_name(if_name):
    if if_name.startswith("Eth") and "Trunk" not in if_name:
        return if_name.replace("Eth", "Ethernet")
    elif if_name.startswith("Fa"):
        return if_name.replace("Fa", "FastEthernet")
    elif if_name.startswith("Gig"):
        return if_name.replace("Gig", "GigabitEthernet")
    elif if_name.startswith("GE"):
        return if_name.replace("GE", "GigabitEthernet")
    elif if_name.startswith("TE"):
        return if_name.replace("TE", "TenGigabitEthernet")
    elif if_name.startswith("Ten"):
        return if_name.replace("Ten", "TenGigabitEthernet")
    elif if_name.startswith("XGE"):
        return if_name.replace("XGE", "TenGigabitEthernet")
    else:
        return if_name


def normalize_if_name_v2(if_name):
    rules = {
        "Eth-Trunk": "Eth-Trunk",
        "Eth": "Ethernet",
        "Fa": "FastEthernet",
        "Gig": "GigabitEthernet",
        "GE": "GigabitEthernet",
        "TE": "TenGigabitEthernet",
        "Ten": "TenGigabitEthernet",
        "XGE": "TenGigabitEthernet",
    }
    for rule, full_name in rules.items():
        if if_name.startswith(rule):
            return if_name.replace(rule, full_name)
    return if_name


for if_name in interfaces:
    print(normalize_if_name_v2(if_name))
