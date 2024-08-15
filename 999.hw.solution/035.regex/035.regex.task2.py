import re

output = """
spanning-tree mode rapid-pvst
spanning-tree logging
spanning-tree extend system-id
spanning-tree pathcost method long
!
lldp run
!
ntp source-interface Loopback0
!
interface Loopback0
 description -= rid =-
 ip address 192.168.1.1 255.255.255.255
!
interface FastEthernet0/1
 switchport access vlan 10
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
 ip address 4.3.2.1 255.255.255.0
 ip access-group acl_tmp_in in
 ip access-group acl_mgmt_out out
!
interface GigabitEthernet0/4
 description mgmt4.core - FastEthernet0/32
 ip address 1.2.3.4 255.255.255.0
 ip access-group acl_mgmt_in in
 ip access-group acl_mgmt_out out
!
line vty 0 4
 password cisco
!
""".strip()


for interface in re.finditer(
    pattern=r"""
    (?<=\n)
    interface\s+(?P<name>\S+)
    (?:
        |ip\s+address\s+(?P<ip>\S+)\s+(?P<mask>\S+)
        |ip\s+access-group\s+(?P<acl_in>\w+)\s+in
        |ip\s+access-group\s+(?P<acl_out>\w+)\s+out
        |.
    )*?\n
    (?!\s)
    """,
    string=output,
    flags=re.DOTALL | re.VERBOSE,
):
    if interface.group("ip") is None:
        continue
    acl_in = interface.group("acl_in")
    acl_out = interface.group("acl_out")
    name = interface.group("name")

    for real_acl, target_acl in zip((acl_in, acl_out), ("acl_mgmt_in", "acl_mgmt_out")):
        if real_acl != target_acl:
            print(f"{name}: некорректный ACL - {real_acl} вместо {target_acl}")
