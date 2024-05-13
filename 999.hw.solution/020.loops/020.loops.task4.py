vlans_to_check = (10, 100, 300, 400, 500, 800)
line = "switchport trunk allowed vlan 100,200,300-500,600"

raw_vlans = line.split()[-1].split(",")
vlans = []
for vlan in raw_vlans:
    if vlan.isdigit():
        vlans.append(int(vlan))
    elif "-" in vlan:
        vlan_start, vlan_end = vlan.split("-")
        vlans.extend(range(int(vlan_start), int(vlan_end) + 1))

print(line)
for vlan in vlans_to_check:
    if vlan in vlans:
        allowed = True
    else:
        allowed = False

    print(f"vlan {vlan} is {'not ' if not allowed else ''}allowed")
