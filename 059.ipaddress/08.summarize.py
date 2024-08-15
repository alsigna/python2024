import ipaddress

ip1 = ipaddress.IPv4Address("192.168.0.0")
ip2 = ipaddress.IPv4Address("192.168.0.100")
print(list(ipaddress.summarize_address_range(ip1, ip2)))
# [
#     IPv4Network("192.168.0.0/26"),
#     IPv4Network("192.168.0.64/27"),
#     IPv4Network("192.168.0.96/30"),
#     IPv4Network("192.168.0.100/32"),
# ]


ip1 = ipaddress.IPv4Address("192.168.0.0")
ip2 = ipaddress.IPv4Address("192.168.0.255")
print(list(ipaddress.summarize_address_range(ip1, ip2)))

# [IPv4Network('192.168.0.0/24')]
