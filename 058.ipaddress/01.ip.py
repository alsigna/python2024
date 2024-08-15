import ipaddress

ip1 = ipaddress.IPv4Address("192.168.1.100")
print(repr(ip1))

ip2 = ipaddress.ip_address("192.168.1.100")
print(repr(ip2))
