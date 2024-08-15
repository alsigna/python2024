import ipaddress

ip = ipaddress.IPv4Address("192.168.1.100")

print(ip.is_loopback)
print(ip.is_multicast)
print(ip.is_private)
