from netaddr import EUI, IPAddress

print(EUI("0007:ECFF:FEE1:5D18"))

mac = EUI(addr="0007.ECE1.5D18")

print("interface id:", mac.eui64())
print("link-local:", mac.ipv6_link_local())
print("ipv6 eui-64:", mac.ipv6(IPAddress("2001:0BB9:AABB:1234::")))
