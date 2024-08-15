import ipaddress

ip = ipaddress.IPv4Address("192.168.1.100")

print(ip > ipaddress.IPv4Address("192.168.1.101"))
print(ip + 10)
