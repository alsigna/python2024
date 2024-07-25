from .abstract import ConfigTree

__all__ = (
    "CiscoConfigTree",
    "HuaweiConfigTree",
)


class CiscoConfigTree(ConfigTree):
    SPACES = " "
    END_OF_SECTION = "exit"
    SECTION_SEPARATOR = "!"
    UNDO = "no"
    JUNK_LINES = [
        r"^\s*!.*$",
        r"^\s+exit-address-family$",
        r"^Building\s+configuration\s+.*$",
        r"^Current\s+configuration\s+.*$",
        r"^end$",
    ]


class HuaweiConfigTree(ConfigTree):
    SPACES = "  "
    END_OF_SECTION = "quit"
    SECTION_SEPARATOR = "#"
    UNDO = "undo"
    JUNK_LINES = [
        r"^\s*#.*$",
    ]


# def assert_basic_creation() -> None:
#     vendor = "cisco"
#     # получаем парсер под вендора
#     ct = ConfigTree.get_class(vendor)
#     root = ct()
#     # или так, потому что мы переопределили __new__
#     _ = ConfigTree(vendor, "no ip http server", root)
#     vlan = ct("interface Vlan1", root)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
#     _ = ct("no shutdown", vlan)

#     assert str(root) == "root", "root is failed"
#     assert str(root.children.get("interface Vlan1")) == "interface Vlan1", "vlan is failed"

#     node = root.children.get("interface Vlan1")
#     ip = node.children.get("ip address 192.168.1.1 255.255.255.0")
#     assert str(ip) == "ip address 192.168.1.1 255.255.255.0", "ip is failed"


# def assert_cisco_config() -> None:
#     vendor = "cisco"
#     ct = ConfigTree.get_class(vendor)
#     root = ct()
#     _ = ct("no ip http server", root)
#     vlan = ct("interface Vlan1", root)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
#     _ = ct("no shutdown", vlan)

#     target_config = dedent(
#         """
#         no ip http server
#         !
#         interface Vlan1
#          ip address 192.168.1.1 255.255.255.0
#          no shutdown
#         !
#         """
#     ).strip()
#     assert root.config == target_config, "cisco config is failed"


# def assert_huawei_config() -> None:
#     vendor = "huawei"
#     ct = ConfigTree.get_class(vendor)
#     root = ct()
#     _ = ct("undo ip http server", root)
#     vlan = ct("interface Vlanif1", root)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
#     _ = ct("undo shutdown", vlan)

#     target_config = dedent(
#         """
#         undo ip http server
#         #
#         interface Vlanif1
#           ip address 192.168.1.1 255.255.255.0
#           undo shutdown
#         #
#         """
#     ).strip()
#     assert root.config == target_config, "huawei config is failed"


# def assert_eq() -> None:
#     vendor = "cisco"
#     ct = ConfigTree.get_class(vendor)
#     root1 = ct()
#     _ = ct("no ip http server", root1)
#     vlan1 = ct("interface Vlan1", root1)
#     _ = ct("no shutdown", vlan1)
#     ip1 = ct("ip address 192.168.1.1 255.255.255.0", vlan1)

#     root2 = ct()
#     _ = ct("no ip http server", root2)
#     vlan1 = ct("interface Vlan1", root2)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
#     _ = ct("no shutdown", vlan1)

#     root3 = ct()
#     _ = ct("no ip http server", root3)
#     vlan1 = ct("interface Vlan2", root3)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
#     _ = ct("no shutdown", vlan1)

#     root4 = ct()
#     _ = ct("no ip http server", root3)
#     vlan1 = ct("interface Vlan1", root3)
#     _ = ct("ip address 192.168.1.2 255.255.255.0", vlan1)
#     _ = ct("no shutdown", vlan1)

#     root5 = ct()
#     _ = ct("no ip http server", root5)
#     vlan1 = ct("interface Vlan1", root5)
#     _ = ct("description test", vlan1)
#     _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
#     _ = ct("no shutdown", vlan1)

#     root6 = ct()
#     _ = ct("no ip http server", root6)
#     vlan2 = ct("interface Vlan2", root6)
#     _ = ct("description test", vlan2)
#     ip2 = ct("ip address 192.168.1.1 255.255.255.0", vlan2)
#     _ = ct("no shutdown", vlan2)

#     assert root1 == root2, "should be eq"
#     assert root1 != root3, "should not be eq (vlan id)"
#     assert root1 != root4, "should not be eq (ip address)"
#     assert root1 != root5, "should not be eq (extra command)"
#     assert vlan1 != vlan2, "should not be eq (different ifname)"
#     assert ip1 != ip2, "should not be eq (different parent path)"


# def assert_parse() -> None:
#     vendor = "cisco"
#     config = dedent(
#         """
#         lldp run
#         !
#         ntp source-interface Loopback0
#         !
#         interface FastEthernet0/1
#          switchport access vlan 10
#          switchport mode access
#          spanning-tree portfast edge
#          spanning-tree bpduguard enable
#         !
#         line vty 0 4
#          password cisco
#         !
#         """
#     ).strip()
#     parser = ConfigTreeParser(vendor)
#     ct = parser.parse(config)
#     assert ct.config == config, "wrong parsing"


# def assert_copy() -> None:
#     vendor = "cisco"
#     config = dedent(
#         """
#         lldp run
#         !
#         ntp source-interface Loopback0
#         !
#         interface FastEthernet0/1
#          switchport access vlan 10
#          switchport mode access
#          spanning-tree portfast edge
#          spanning-tree bpduguard enable
#         !
#         line vty 0 4
#          password cisco
#         !
#         """
#     ).strip()
#     parser = ConfigTreeParser(vendor)
#     ct1 = parser.parse(config)
#     ct2 = ct1.copy()
#     assert ct1.config == ct2.config, "wrong copy"

#     config = dedent(
#         """
#         license udi pid CSR1000V sn 9BZNE1T61US
#         diagnostic bootup level minimal
#         archive
#          log config
#           logging enable 1
#            level 1-1
#             level 1-2
#           logging enable 2
#            level 2-1
#             level 2-2
#         memory free low-watermark processor 71497
#         !
#         spanning-tree extend system-id
#         !
#         """
#     ).strip()
#     logging_with_children_config = dedent(
#         """
#         archive
#          log config
#           logging enable 1
#            level 1-1
#             level 1-2
#         !
#         """
#     ).strip()
#     logging_without_children_config = dedent(
#         """
#         archive
#          log config
#           logging enable 1
#         !
#         """
#     ).strip()

#     ct = parser.parse(config)
#     logging = ct.children["archive"].children["log config"].children["logging enable 1"]
#     logging_with_children = logging.copy()
#     logging_without_children = logging.copy(children=False)
#     assert logging_with_children.config == logging_with_children_config, "wrond copy with children"
#     assert logging_without_children.config == logging_without_children_config, "wrond copy without children"


# def assert_cisco_patch() -> None:
#     vendor = "cisco"
#     config = dedent(
#         """
#         !
#         router ospf 101
#          router-id 1.1.1.101
#          network 10.1.0.0 0.0.0.255 area 0
#         !
#         router bgp 65000
#          bgp router-id 10.255.255.101
#          neighbor 4.3.2.1 remote-as 65000
#          neighbor 10.255.255.102 remote-as 65000
#          neighbor 10.255.255.102 update-source Loopback0
#          !
#          address-family ipv4
#           network 100.64.255.101 mask 255.255.255.255
#           no neighbor 4.3.2.1 activate
#           neighbor 10.255.255.102 activate
#          exit-address-family
#          !
#          address-family vpnv4 unicast
#           no neighbor 1.2.3.4 activate
#          exit-address-family
#         !
#         ip forward-protocol nd
#         no ip http server
#         ip http secure-server
#         !
#         """
#     ).strip()

#     target = dedent(
#         """
#         router ospf 101
#         router-id 1.1.1.101
#         network 10.1.0.0 0.0.0.255 area 0
#         exit
#         router bgp 65000
#         bgp router-id 10.255.255.101
#         neighbor 4.3.2.1 remote-as 65000
#         neighbor 10.255.255.102 remote-as 65000
#         neighbor 10.255.255.102 update-source Loopback0
#         address-family ipv4
#         network 100.64.255.101 mask 255.255.255.255
#         no neighbor 4.3.2.1 activate
#         neighbor 10.255.255.102 activate
#         exit
#         address-family vpnv4 unicast
#         no neighbor 1.2.3.4 activate
#         exit
#         exit
#         ip forward-protocol nd
#         no ip http server
#         ip http secure-server
#         """
#     ).strip()
#     ct = ConfigTreeParser.vendor_parse(vendor, config)
#     assert ct.patch == target, "wrong patch"


# def assert_huawei_patch() -> None:
#     vendor = "huawei"
#     config = dedent(
#         """
#         #
#         router ospf 101
#          router-id 1.1.1.101
#          network 10.1.0.0 0.0.0.255 area 0
#         #
#         router bgp 65000
#          bgp router-id 10.255.255.101
#          neighbor 4.3.2.1 remote-as 65000
#          neighbor 10.255.255.102 remote-as 65000
#          neighbor 10.255.255.102 update-source Loopback0
#          #
#          address-family ipv4
#           network 100.64.255.101 mask 255.255.255.255
#           no neighbor 4.3.2.1 activate
#           neighbor 10.255.255.102 activate
#          exit-address-family
#          #
#          address-family vpnv4 unicast
#           no neighbor 1.2.3.4 activate
#          exit-address-family
#         #
#         ip forward-protocol nd
#         no ip http server
#         ip http secure-server
#         #
#         """
#     ).strip()

#     target = dedent(
#         """
#         router ospf 101
#         router-id 1.1.1.101
#         network 10.1.0.0 0.0.0.255 area 0
#         quit
#         router bgp 65000
#         bgp router-id 10.255.255.101
#         neighbor 4.3.2.1 remote-as 65000
#         neighbor 10.255.255.102 remote-as 65000
#         neighbor 10.255.255.102 update-source Loopback0
#         address-family ipv4
#         network 100.64.255.101 mask 255.255.255.255
#         no neighbor 4.3.2.1 activate
#         neighbor 10.255.255.102 activate
#         quit
#         address-family vpnv4 unicast
#         no neighbor 1.2.3.4 activate
#         quit
#         quit
#         ip forward-protocol nd
#         no ip http server
#         ip http secure-server
#         """
#     ).strip()
#     ct = ConfigTreeParser.vendor_parse(vendor, config)
#     assert ct.patch == target, "wrong patch"


# def assert_merge() -> None:
#     vendor = "cisco"
#     config1 = dedent(
#         """
#         no ip http server
#         !
#         interface Vlan1
#           ip address 192.168.1.1 255.255.255.0
#           no shutdown
#         !
#         """
#     ).strip()
#     config2 = dedent(
#         """
#         no ip http server
#         !
#         interface Vlan2
#           ip address 192.168.2.1 255.255.255.0
#         !
#         """
#     ).strip()
#     config3 = dedent(
#         """
#         interface Vlan2
#           description my vlan
#           ip address 192.168.3.1 255.255.255.0 secondary
#         !
#         """
#     ).strip()
#     merged_config = dedent(
#         """
#         no ip http server
#         !
#         interface Vlan1
#          ip address 192.168.1.1 255.255.255.0
#          no shutdown
#         !
#         interface Vlan2
#          ip address 192.168.2.1 255.255.255.0
#          description my vlan
#          ip address 192.168.3.1 255.255.255.0 secondary
#         !
#         """
#     ).strip()
#     parser = ConfigTreeParser(vendor)
#     ct1 = parser.parse(config1)
#     ct2 = parser.parse(config2)
#     ct3 = parser.parse(config3)
#     ct1.merge(ct2)
#     ct1.merge(ct3)
#     assert ct1.config == merged_config, "wrong merge"


# def main() -> None:
#     with open("./cisco_run.txt", "r") as f:
#         cisco_cfg = f.read()

#     with open("./huawei_run.txt", "r") as f:
#         huawei_cfg = f.read()

#     ct_cisco = ConfigTreeParser.vendor_parse("cisco", cisco_cfg)
#     ct_huawei = ConfigTreeParser.vendor_parse("huawei", huawei_cfg)

#     print(ct_cisco.config)
#     print(ct_cisco.patch)
#     print("---")
#     print(ct_huawei.config)
#     print(ct_huawei.patch)


# if __name__ == "__main__":
#     assert_basic_creation()
#     assert_cisco_config()
#     assert_huawei_config()
#     assert_eq()
#     assert_parse()
#     assert_copy()
#     assert_cisco_patch()
#     assert_huawei_patch()
#     assert_merge()
#     main()
