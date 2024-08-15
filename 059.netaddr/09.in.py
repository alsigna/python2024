from netaddr import IPAddress, IPNetwork

net = IPNetwork("192.168.0.0/23")
ip1 = IPAddress("192.168.1.100")
ip2 = IPAddress("192.168.2.100")

print(ip1 in net)
print(ip2 in net)
