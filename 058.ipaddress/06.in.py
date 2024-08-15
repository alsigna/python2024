import ipaddress

net = ipaddress.IPv4Network("192.168.1.100/23", strict=False)

ip = ipaddress.IPv4Address("192.168.0.2")
print(ip in net)


ip = ipaddress.IPv4Address("192.168.2.2")
print(ip in net)
