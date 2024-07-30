from scrapli_replay.server.collector import ScrapliCollector

host = "192.168.122.101"
device = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ]
    },
}

collector = ScrapliCollector(
    channel_inputs=[
        "show version",
        "show ip int br",
        "sh lacp ne",
        "sh ip ospf ne",
    ],
    interact_events=[
        [
            ("clear logging", "[confirm]", False),
            ("", "#", False),
        ],
    ],
    paging_indicator="--More--",
    paging_escape_string="\x1b",
    collector_session_filename=f"collector_session_dump_{host}.yaml",
    host=host,
    **device,
)

collector.open()
collector.collect()
collector.close()
collector.dump()
