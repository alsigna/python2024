from collections import namedtuple

config = """
spanning-tree mode rapid-pvst
spanning-tree logging
spanning-tree extend system-id
spanning-tree pathcost method long
!
lldp run
!
interface FastEthernet0/1
 switchport access vlan 10
 switchport mode access
 spanning-tree portfast edge
 spanning-tree bpduguard enable
!
interface FastEthernet0/2
 switchport access vlan 11
 switchport mode access
 spanning-tree portfast edge
 spanning-tree bpduguard enable
!
interface FastEthernet0/3
 switchport access vlan 51
 switchport mode access
 spanning-tree portfast edge
 spanning-tree bpduguard enable
!
interface FastEthernet0/4
 switchport mode access
 spanning-tree portfast edge
 spanning-tree bpduguard enable
!
interface GigabitEthernet0/1
 description mgmt1.core - FastEthernet0/32
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50-70,80,90
 mls qos trust cos
 ip dhcp snooping trust
!
interface GigabitEthernet0/2
 description mgmt2.core - FastEthernet0/32
 switchport mode trunk
 mls qos trust cos
 ip dhcp snooping trust
!
interface GigabitEthernet0/3
  description mgmt3.core - FastEthernet0/32
  switchport mode trunk
  switchport trunk allowed vlan 10,20,30,40,50-70,80,90
  switchport trunk allowed vlan add 150,151
  mls qos trust cos
  ip dhcp snooping trust
!
interface GigabitEthernet0/4
 description mgmt4.core - FastEthernet0/32
 ip address 1.2.3.4 255.255.255.0
!
line vty 0 4
 password cisco
!
"""

Interface = namedtuple("Interface", ("name", "mode", "vlans"))
lines = config.splitlines()
# на случай, если в конфигурации последняя секция не закрыта
lines.append("!")

current_interface = ""
mode = ""
vlans = []
vlans_per_interface = {}

# заполняем словарь vlans_per_interface вида {<interface_name>: Interface(name, mode, vlans)}
for line in lines:
    if current_interface and not line.startswith(" "):
        if mode == "access" and len(vlans) == 0:
            vlans.append(1)
        elif mode == "trunk" and len(vlans) == 0:
            # vlans.extend(range(1, 4097))
            vlans.append(0)
        if mode:
            vlans_per_interface[current_interface] = Interface(
                name=current_interface,
                mode=mode,
                vlans=vlans,
            )
        mode = ""
        current_interface = ""
        vlans = []

    line = line.strip()
    if line.startswith("interface"):
        current_interface = line.split(maxsplit=1)[-1]
    elif line.startswith("switchport mode"):
        mode = line.split()[-1]
    elif line.startswith("switchport access vlan"):
        vlan = line.split()[-1]
        vlans.append(int(vlan))
    elif line.startswith("switchport trunk allowed vlan"):
        trunk_vlans = line.split()[-1].split(",")
        for vlan in trunk_vlans:
            if vlan.isdigit():
                vlans.append(int(vlan))
            elif "-" in vlan:
                vlan_start, vlan_end = vlan.split("-")
                vlan_list = range(int(vlan_start), int(vlan_end) + 1)
                vlans.extend(vlan_list)

# проверяем на каких интерфейсах разрешен каждый из vlan из набора vlans_to_check
vlans_to_check = (1, 3, 11, 30, 54, 150, 300)
for vlan in vlans_to_check:
    print("-" * 10, f"проверка vlan {vlan}", "-" * 10)
    for interface in vlans_per_interface.values():
        if vlan in interface.vlans:
            allowed = True
        # если вместо range(1, 4097) мы для всех vlan используем 0, тогда нужна эта ветка
        elif len(interface.vlans) == 1 and interface.vlans[0] == 0:
            allowed = True
        else:
            allowed = False

        if allowed:
            print(f"vlan {vlan} разрешен на интерфейсе {interface.name}")


# используя шаблоны можем собрать конфигурацию интерфейса на основе его данных
access = """
interface {name}
   switchport mode access
   switchport access vlan {vlan}
!
""".strip()

trunk = """
interface {name}
   switchport mode trunk
   switchport trunk allowed vlan {vlan}
!
""".strip()

templates = {"access": access, "trunk": trunk}

for interface in vlans_per_interface.values():
    template = templates.get(interface.mode)
    if template is None:
        continue
    vlan = ",".join(map(str, interface.vlans))
    config = template.format(name=interface.name, vlan=vlan)
    print(config)
