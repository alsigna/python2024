from netaddr import IPAddress, cidr_merge, valid_ipv4

print(valid_ipv4("192.168.1.100"))
print(valid_ipv4("192.168.1.300"))
