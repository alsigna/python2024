from typing import Generator

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
line vty 0 4
 password cisco
!
""".strip()


def config_generator(config: str) -> Generator[str, None, None]:
    for line in config.strip().splitlines():
        if line.strip() in ["!", "exit-address-family"]:
            continue
        else:
            yield line


print("-" * 10, "config_generator", "-" * 10)

for line in config_generator(config):
    print(line)


def patch_generator(config: str) -> Generator[str, None, None]:
    last_space = 0
    for line in config.strip().splitlines():
        current_space = len(line) - len(line.lstrip())
        if current_space < last_space:
            last_space = current_space
            yield "exit"
        last_space = current_space
        if line.strip() in ["!", "exit-address-family"]:
            continue
        else:
            yield line.strip()


print("-" * 10, "patch_generator", "-" * 10)

for line in patch_generator(config):
    print(line)
