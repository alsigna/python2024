# Есть входная строка

# ```python
# output = "switchport trunk allowed vlan 2,101,104"
# ```

# Нужно получить список vlan (типа int).

# ```python
# vlans
# >>> [2, 101, 104]
# ```

output = "switchport trunk allowed vlan 2,101,104"

vlans_str = output.split()[-1]
vlans_list = vlans_str.split(",")
# без циклов/map только явным перебором
vlans = [
    int(vlans_list[0]),
    int(vlans_list[1]),
    int(vlans_list[2]),
]
