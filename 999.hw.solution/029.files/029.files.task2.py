from pathlib import Path

rt01_config = """
!
interface Vlan1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
line vty 0 4
 password cisco
!
""".strip()

rt02_config = """
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
""".strip()

configs = {
    "rt01": rt01_config,
    "rt02": rt02_config,
}


def save_configs(configs: dict[str, str], folder: Path = Path("configs")) -> None:
    if not folder.is_absolute():
        folder = Path(Path.cwd(), folder)

    folder.mkdir(parents=True, exist_ok=True)

    for hostname, config in configs.items():
        filename = Path(folder, f"{hostname}.txt")
        with open(filename, "w") as f:
            f.write(config)


save_configs(configs)
# save_configs(configs, Path("my_configs-1", "my_configs-2"))
# save_configs(configs, Path("/Users/alexigna/Desktop/python/my_configs-2"))
# save_configs(configs, Path(Path.cwd(), "my_configs-1", "my_configs-2"))
