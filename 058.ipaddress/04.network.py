import ipaddress

net = ipaddress.IPv4Network("192.168.1.100/24", strict=False)

print(repr(net))


print("адрес сети:", net.network_address)
print("маска сети:", net.netmask)
print("длина маски:", net.prefixlen)
print("wildcard маска:", net.hostmask)
print("broadcast адрес:", net.broadcast_address)
