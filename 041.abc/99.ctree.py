from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections import deque
from textwrap import dedent


class AbstractConfigTree(ABC):
    __slots__ = ["line", "parent", "children"]

    @property
    @abstractmethod
    def SPACES(self) -> str:
        """количество пробелов для нового уровня"""

    @property
    @abstractmethod
    def END_OF_SECTION(self) -> str:
        pass

    @property
    @abstractmethod
    def SECTION_SEPARATOR(self) -> str:
        pass

    def __init__(self, line: str = "", parent: AbstractConfigTree | None = None) -> None:
        self.line = line
        self.parent = parent
        self.children: dict[str, AbstractConfigTree] = {}
        if parent is not None:
            parent.children[line] = self

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        return f"({id(self)}) '{str(self)}'"

    def __eq__(self, other: AbstractConfigTree) -> bool:
        if self.line != other.line:
            return False
        if len(self.children) != len(other.children):
            return False

        self_parents = []

        p = self.parent
        while p is not None:
            self_parents.append(p.line)
            p = p.parent

        other_parents = []
        p = other.parent
        while p is not None:
            other_parents.append(p.line)
            p = p.parent

        if self_parents != other_parents:
            return False

        children_eq = []
        for line, node in self.children.items():
            other_node = other.children.get(line)
            if other_node is None:
                return False
            children_eq.append(node == other_node)
        return all(children_eq)

    def _config(self, symbol: str, level: int) -> str:
        result = [symbol * level + self.line]
        for child in self.children.values():
            result.extend(child._config(symbol=symbol, level=level + 1))
        return result

    @property
    def config(self) -> str:
        result = []
        level = 0
        node = self
        while node.parent is not None:
            result.append(node.line)
            level += 1
            node = node.parent
        result.reverse()
        result = [self.SPACES * l + line for l, line in enumerate(result)]
        for child in self.children.values():
            result.extend(child._config(symbol=self.SPACES, level=level))
            result.append(self.SECTION_SEPARATOR)
        return "\n".join(result)

    @property
    def patch(self) -> str:
        nodes = deque(self.children.values())
        result = []
        path_to_root = []

        node = self
        while node.parent is not None:
            path_to_root.append(node.line)
            node = node.parent
        path_to_root.reverse()

        while len(nodes) > 0:
            node = nodes.popleft()
            result.append(node.line)
            if len(node.children) != 0:
                nodes.appendleft(self.__class__(line=self.END_OF_SECTION))
                nodes.extendleft(list(node.children.values())[::-1])
        result = path_to_root + result + [self.END_OF_SECTION] * len(path_to_root)
        return "\n".join(result)

    def _copy(self, children: bool, parent: AbstractConfigTree | None) -> AbstractConfigTree:
        if self.parent is not None and parent is None:
            parent = self.parent._copy(children=False, parent=None)

        new_obj = self.__class__(line=self.line, parent=parent)
        if children:
            for child in self.children.values():
                _ = child._copy(children, new_obj)
        return new_obj

    def copy(self, children: bool = True) -> AbstractConfigTree:
        root = self._copy(children=children, parent=None)
        while root.parent is not None:
            root = root.parent
        return root

    def merge(self, other: AbstractConfigTree) -> None:
        for line, node in other.children.items():
            if line not in self.children:
                _ = node._copy(children=True, parent=self)
            else:
                self.children[line].merge(node)


class CiscoConfigTree(AbstractConfigTree):
    SPACES = " "
    END_OF_SECTION = "exit"
    SECTION_SEPARATOR = "!"


class HuaweiConfigTree(AbstractConfigTree):
    SPACES = "  "
    END_OF_SECTION = "quit"
    SECTION_SEPARATOR = "#"


class ConfigTree:
    VENDOR_MAP = {
        "cisco": CiscoConfigTree,
        "huawei": HuaweiConfigTree,
    }

    def __new__(cls, vendor: str, line: str = "", parent: AbstractConfigTree | None = None) -> AbstractConfigTree:
        _class: AbstractConfigTree = cls.get_class(vendor)
        node = _class(line=line, parent=parent)
        return node

    @classmethod
    def get_class(cls, vendor: str):
        _class = cls.VENDOR_MAP.get(vendor)
        if _class is None:
            raise NotImplementedError("unknown vendor")
        return _class


class ConfigTreeParser:
    SKIP_LINES = [
        r"^\s*!.*$",
        r"^\s*#.*$",
        r"^\s+exit-address-family$",
        r"^Building\s+configuration\s+.*$",
        r"^Current\s+configuration\s+.*$",
    ]

    def __init__(self, vendor: str) -> None:
        self._parser = ConfigTree.get_class(vendor)

    @classmethod
    def _parse(cls, ct: AbstractConfigTree, config: str) -> AbstractConfigTree:
        root = ct()
        section = [root]
        spaces = [0]
        for line in config.splitlines():
            if len(line.strip()) == 0:
                continue
            skip = [re.fullmatch(p, line) for p in cls.SKIP_LINES]
            if any(skip):
                continue

            # число пробелов у текущей строки
            current_space = len(line) - len(line.lstrip())

            # мы вошли в секцию
            if current_space > spaces[-1]:
                node = list(section[-1].children.values())[-1]
                section.append(node)
                spaces.append(current_space)
            # мы вышли из секции
            elif current_space < spaces[-1]:
                while current_space != spaces[-1]:
                    _ = section.pop()
                    _ = spaces.pop()
            _ = ct(line.lstrip(), section[-1])
        return root

    @classmethod
    def vendor_parse(cls, vendor: str, config: str) -> AbstractConfigTree:
        _parser = ConfigTree.get_class(vendor)
        root = cls._parse(_parser, config)
        return root

    def parse(self, config: str) -> AbstractConfigTree:
        root = self._parse(self._parser, config)
        return root


def assert_basic_creation() -> None:
    vendor = "cisco"
    # получаем парсер под вендора
    ct = ConfigTree.get_class(vendor)
    root = ct()
    # или так, потому что мы переопределили __new__
    _ = ConfigTree(vendor, "no ip http server", root)
    vlan = ct("interface Vlan1", root)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ct("no shutdown", vlan)

    assert str(root) == "root", "root is failed"
    assert str(root.children.get("interface Vlan1")) == "interface Vlan1", "vlan is failed"

    node = root.children.get("interface Vlan1")
    ip = node.children.get("ip address 192.168.1.1 255.255.255.0")
    assert str(ip) == "ip address 192.168.1.1 255.255.255.0", "ip is failed"


def assert_cisco_config() -> None:
    vendor = "cisco"
    ct = ConfigTree.get_class(vendor)
    root = ct()
    _ = ct("no ip http server", root)
    vlan = ct("interface Vlan1", root)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ct("no shutdown", vlan)

    target_config = dedent(
        """
        no ip http server
        !
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         no shutdown
        !
        """
    ).strip()
    assert root.config == target_config, "cisco config is failed"


def assert_huawei_config() -> None:
    vendor = "huawei"
    ct = ConfigTree.get_class(vendor)
    root = ct()
    _ = ct("undo ip http server", root)
    vlan = ct("interface Vlanif1", root)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ct("undo shutdown", vlan)

    target_config = dedent(
        """
        undo ip http server
        #
        interface Vlanif1
          ip address 192.168.1.1 255.255.255.0
          undo shutdown
        #
        """
    ).strip()
    assert root.config == target_config, "huawei config is failed"


def assert_eq() -> None:
    vendor = "cisco"
    ct = ConfigTree.get_class(vendor)
    root1 = ct()
    _ = ct("no ip http server", root1)
    vlan1 = ct("interface Vlan1", root1)
    _ = ct("no shutdown", vlan1)
    ip1 = ct("ip address 192.168.1.1 255.255.255.0", vlan1)

    root2 = ct()
    _ = ct("no ip http server", root2)
    vlan1 = ct("interface Vlan1", root2)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
    _ = ct("no shutdown", vlan1)

    root3 = ct()
    _ = ct("no ip http server", root3)
    vlan1 = ct("interface Vlan2", root3)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
    _ = ct("no shutdown", vlan1)

    root4 = ct()
    _ = ct("no ip http server", root3)
    vlan1 = ct("interface Vlan1", root3)
    _ = ct("ip address 192.168.1.2 255.255.255.0", vlan1)
    _ = ct("no shutdown", vlan1)

    root5 = ct()
    _ = ct("no ip http server", root5)
    vlan1 = ct("interface Vlan1", root5)
    _ = ct("description test", vlan1)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan1)
    _ = ct("no shutdown", vlan1)

    root6 = ct()
    _ = ct("no ip http server", root6)
    vlan2 = ct("interface Vlan2", root6)
    _ = ct("description test", vlan2)
    ip2 = ct("ip address 192.168.1.1 255.255.255.0", vlan2)
    _ = ct("no shutdown", vlan2)

    assert root1 == root2, "should be eq"
    assert root1 != root3, "should not be eq (vlan id)"
    assert root1 != root4, "should not be eq (ip address)"
    assert root1 != root5, "should not be eq (extra command)"
    assert vlan1 != vlan2, "should not be eq (different ifname)"
    assert ip1 != ip2, "should not be eq (different parent path)"


def assert_parse() -> None:
    vendor = "cisco"
    config = dedent(
        """
        lldp run
        !
        ntp source-interface Loopback0
        !
        interface FastEthernet0/1
         switchport access vlan 10
         switchport mode access
         spanning-tree portfast edge
         spanning-tree bpduguard enable
        !
        line vty 0 4
         password cisco
        !
        """
    ).strip()
    parser = ConfigTreeParser(vendor)
    ct = parser.parse(config)
    assert ct.config == config, "wrong parsing"


def assert_copy() -> None:
    vendor = "cisco"
    config = dedent(
        """
        lldp run
        !
        ntp source-interface Loopback0
        !
        interface FastEthernet0/1
         switchport access vlan 10
         switchport mode access
         spanning-tree portfast edge
         spanning-tree bpduguard enable
        !
        line vty 0 4
         password cisco
        !
        """
    ).strip()
    parser = ConfigTreeParser(vendor)
    ct1 = parser.parse(config)
    ct2 = ct1.copy()
    assert ct1.config == ct2.config, "wrong copy"

    config = dedent(
        """
        license udi pid CSR1000V sn 9BZNE1T61US
        diagnostic bootup level minimal
        archive
         log config
          logging enable 1
           level 1-1
            level 1-2
          logging enable 2
           level 2-1
            level 2-2
        memory free low-watermark processor 71497
        !
        spanning-tree extend system-id
        !
        """
    ).strip()
    logging_with_children_config = dedent(
        """
        archive
         log config
          logging enable 1
           level 1-1
            level 1-2
        !
        """
    ).strip()
    logging_without_children_config = dedent(
        """
        archive
         log config
          logging enable 1
        !
        """
    ).strip()

    ct = parser.parse(config)
    logging = ct.children["archive"].children["log config"].children["logging enable 1"]
    logging_with_children = logging.copy()
    logging_without_children = logging.copy(children=False)
    assert logging_with_children.config == logging_with_children_config, "wrond copy with children"
    assert logging_without_children.config == logging_without_children_config, "wrond copy without children"


def assert_cisco_patch() -> None:
    vendor = "cisco"
    config = dedent(
        """
        !
        router ospf 101
         router-id 1.1.1.101
         network 10.1.0.0 0.0.0.255 area 0
        !
        router bgp 65000
         bgp router-id 10.255.255.101
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
         address-family vpnv4 unicast
          no neighbor 1.2.3.4 activate
         exit-address-family
        !
        ip forward-protocol nd
        no ip http server
        ip http secure-server
        !
        """
    ).strip()

    target = dedent(
        """
        router ospf 101
        router-id 1.1.1.101
        network 10.1.0.0 0.0.0.255 area 0
        exit
        router bgp 65000
        bgp router-id 10.255.255.101
        neighbor 4.3.2.1 remote-as 65000
        neighbor 10.255.255.102 remote-as 65000
        neighbor 10.255.255.102 update-source Loopback0
        address-family ipv4
        network 100.64.255.101 mask 255.255.255.255
        no neighbor 4.3.2.1 activate
        neighbor 10.255.255.102 activate
        exit
        address-family vpnv4 unicast
        no neighbor 1.2.3.4 activate
        exit
        exit
        ip forward-protocol nd
        no ip http server
        ip http secure-server
        """
    ).strip()
    ct = ConfigTreeParser.vendor_parse(vendor, config)
    assert ct.patch == target, "wrong patch"


def assert_huawei_patch() -> None:
    vendor = "huawei"
    config = dedent(
        """
        #
        router ospf 101
         router-id 1.1.1.101
         network 10.1.0.0 0.0.0.255 area 0
        #
        router bgp 65000
         bgp router-id 10.255.255.101
         neighbor 4.3.2.1 remote-as 65000
         neighbor 10.255.255.102 remote-as 65000
         neighbor 10.255.255.102 update-source Loopback0
         #
         address-family ipv4
          network 100.64.255.101 mask 255.255.255.255
          no neighbor 4.3.2.1 activate
          neighbor 10.255.255.102 activate
         exit-address-family
         #
         address-family vpnv4 unicast
          no neighbor 1.2.3.4 activate
         exit-address-family
        #
        ip forward-protocol nd
        no ip http server
        ip http secure-server
        #
        """
    ).strip()

    target = dedent(
        """
        router ospf 101
        router-id 1.1.1.101
        network 10.1.0.0 0.0.0.255 area 0
        quit
        router bgp 65000
        bgp router-id 10.255.255.101
        neighbor 4.3.2.1 remote-as 65000
        neighbor 10.255.255.102 remote-as 65000
        neighbor 10.255.255.102 update-source Loopback0
        address-family ipv4
        network 100.64.255.101 mask 255.255.255.255
        no neighbor 4.3.2.1 activate
        neighbor 10.255.255.102 activate
        quit
        address-family vpnv4 unicast
        no neighbor 1.2.3.4 activate
        quit
        quit
        ip forward-protocol nd
        no ip http server
        ip http secure-server
        """
    ).strip()
    ct = ConfigTreeParser.vendor_parse(vendor, config)
    assert ct.patch == target, "wrong patch"


def assert_merge() -> None:
    vendor = "cisco"
    config1 = dedent(
        """
        no ip http server
        !
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        !
        """
    ).strip()
    config2 = dedent(
        """
        no ip http server
        !
        interface Vlan2
          ip address 192.168.2.1 255.255.255.0
        !
        """
    ).strip()
    config3 = dedent(
        """
        interface Vlan2
          description my vlan
          ip address 192.168.3.1 255.255.255.0 secondary
        !
        """
    ).strip()
    merged_config = dedent(
        """
        no ip http server
        !
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         no shutdown
        !
        interface Vlan2
         ip address 192.168.2.1 255.255.255.0
         description my vlan
         ip address 192.168.3.1 255.255.255.0 secondary
        !
        """
    ).strip()
    parser = ConfigTreeParser(vendor)
    ct1 = parser.parse(config1)
    ct2 = parser.parse(config2)
    ct3 = parser.parse(config3)
    ct1.merge(ct2)
    ct1.merge(ct3)
    assert ct1.config == merged_config, "wrong merge"


def main() -> None:
    with open("./cisco_run.txt", "r") as f:
        cisco_cfg = f.read()

    with open("./huawei_run.txt", "r") as f:
        huawei_cfg = f.read()

    ct_cisco = ConfigTreeParser.vendor_parse("cisco", cisco_cfg)
    ct_huawei = ConfigTreeParser.vendor_parse("huawei", huawei_cfg)

    print(ct_cisco.config)
    print(ct_cisco.patch)
    print("---")
    print(ct_huawei.config)
    print(ct_huawei.patch)


if __name__ == "__main__":
    assert_basic_creation()
    assert_cisco_config()
    assert_huawei_config()
    assert_eq()
    assert_parse()
    assert_copy()
    assert_cisco_patch()
    assert_huawei_patch()
    assert_merge()
    main()
