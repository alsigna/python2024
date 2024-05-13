devices = [
    "rt1.lan.hq.net",
    "p1.mpls.hq.net",
    "p2.mpls.hq.net",
    "sw1.lan.hq.net",
    "dsw1.lan.hq.net",
]

print(
    [device for device in devices if device.endswith("lan.hq.net")],
)
