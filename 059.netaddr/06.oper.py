from netaddr import IPAddress

ip = IPAddress("192.168.1.1")

print(ip > IPAddress("192.168.1.0"))

print(ip + 10)
