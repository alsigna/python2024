vlans_str = "10,21"
vlans_int = list(map(int, vlans_str.split(",")))
vlans_int.sort()

vlans = []
start = vlans_int[0]
end = vlans_int[0]

for vlan in vlans_int[1:]:
    if vlan == end + 1:
        end = vlan
    else:
        if start == end:
            vlans.append(f"{start}")
        else:
            vlans.append(f"{start}-{end}")
        start = vlan
    end = vlan

vlans.append(str(start) if start == end else f"{start}-{end}")

result = ",".join(vlans)
print(result)
