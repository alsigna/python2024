from ctree import ConfigTreeDiffer, ConfigTreeFactory, ConfigTreeParser, Vendor

ct = ConfigTreeFactory.get_class(Vendor.CISCO)

root = ct()
_ = ct("no ip http server", root)
vlan = ct("interface Vlan1", root)
_ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
_ = ct("no shutdown", vlan)


assert str(root) == "root", "root is failed"
assert str(root.children.get("interface Vlan1")) == "interface Vlan1", "vlan is failed"


config_a = """
!
interface GigabitEthernet8
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
router ospf 1
 router-id 10.255.255.101
 passive-interface Loopback0
 network 10.255.12.1 0.0.0.0 area 0
 network 10.255.255.101 0.0.0.0 area 0
!
router ospf 101
 router-id 1.1.1.101
 network 10.1.0.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
 network 10.1.2.0 0.0.0.255 area 0
!
router bgp 65000
 bgp router-id 10.255.255.101
 bgp log-neighbor-changes
 neighbor 4.3.2.1 remote-as 65000
 neighbor 10.255.255.102 remote-as 65000
 neighbor 10.255.255.102 update-source Loopback0
 !
 address-family ipv4
  network 100.64.255.101 mask 255.255.255.255
  no neighbor 4.3.2.1 activate
  neighbor 10.255.255.102 activate
 exit-address-family
!
ip forward-protocol nd
no ip http server
ip http secure-server
!
ip route vrf mgmt 10.8.0.0 255.255.255.0 192.168.122.1
ip ssh rsa keypair-name SSH
!
""".strip()

config_b = """
!
interface GigabitEthernet8
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
router ospf 1
 router-id 10.255.255.101
 passive-interface Loopback0
 network 10.255.12.1 0.0.0.0 area 0
 network 10.255.255.101 0.0.0.0 area 0
!
router ospf 101
 router-id 1.1.1.101
 network 10.1.0.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.255 area 0
 network 10.1.2.0 0.0.0.255 area 0
!
router bgp 65000
 bgp router-id 10.255.255.101
 bgp log-neighbor-changes
 neighbor 4.3.2.1 remote-as 65000
 neighbor 10.255.255.103 remote-as 65000
 neighbor 10.255.255.103 update-source Loopback0
 !
 address-family ipv4
  network 100.64.255.101 mask 255.255.255.255
  no neighbor 4.3.2.1 activate
  neighbor 10.255.255.103 activate
 exit-address-family
!
ip forward-protocol nd
no ip http server
ip http secure-server
!
ip route vrf mgmt 10.8.0.0 255.255.255.0 192.168.122.1
ip ssh rsa keypair-name SSH
!
""".strip()

ct_a = ConfigTreeParser.vendor_parse(Vendor.CISCO, config_a)
ct_b = ConfigTreeParser.vendor_parse(Vendor.CISCO, config_b)

ct = ConfigTreeDiffer.diff(ct_a, ct_b)
print(ct.config)
print("---")
print(ct.patch)
