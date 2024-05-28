from pprint import pprint

config = """
!
interface Vlan1
 no ip address
 shutdown
!
vlan 2
 name LAN
!
interface Vlan2
 description -= LAN =-
 ip address 192.168.1.1 255.255.255.0
 ip helper-address 172.16.100.100
 no ip proxy-arp
 ip mtu 1272
 ip tcp adjust-mss 1232
 load-interval 30
 no shutdown
!
router bgp 64512
 bgp router-id 10.255.1.2
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor ACTIVE peer-group
 neighbor ACTIVE remote-as 64512
 neighbor ACTIVE description -= primary session =-
 neighbor ACTIVE fall-over bfd
 neighbor BACKUP peer-group
 neighbor BACKUP remote-as 64512
 neighbor BACKUP description -= backup session =-
 neighbor 1.2.3.4 peer-group BACKUP
 neighbor 4.3.2.1 peer-group ACTIVE
 !
 address-family ipv4
  redistribute connected route-map LAN
  neighbor ACTIVE send-community both
  neighbor BACKUP send-community both
  neighbor 1.2.3.4 activate
  neighbor 4.3.2.1 activate
  maximum-paths 2
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 1.2.3.4 activate
  neighbor 4.3.2.1 activate
 exit-address-family
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
ip bgp-community new-format
!
""".strip()


config = """
ip forward-protocol nd
no ip http server
!
interface Vlan1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
router bgp 64512
 bgp router-id 192.168.1.1
 bgp log-neighbor-changes
 !
 address-family ipv4
  redistribute connected route-map LAN
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 1.2.3.4 activate
 exit-address-family
!
interface loopbak0
 ip address 192.168.2.1 255.255.255.255
 some new sub-level
  sub-level-1
   sub-level-2
    sub-level-3
   sub-level-4
!
""".strip()
JUNK_COMMANDS = ["!", "exit-address-family"]


def parse_config(config: str) -> dict[str, dict]:
    def get_result() -> dict[str, dict]:
        if len(sub_block) != 0:
            return parse_config("\n".join(sub_block))
        else:
            return {}

    result: dict[str, dict] = {}

    block = ""
    sub_block: list[str] = []
    space_count = 0

    for line in config.splitlines():
        if line.strip() in JUNK_COMMANDS:
            continue
        if not line.startswith(" "):
            if block:
                result[block] = get_result()
                space_count = 0
            block = line.strip()
            sub_block = []
        else:
            if not space_count:
                space_count = len(line) - len(line.lstrip())
            line = line.removeprefix(" " * space_count)
            sub_block.append(line)
    if block:
        result[block] = get_result()

    return result


pprint(parse_config(config))
