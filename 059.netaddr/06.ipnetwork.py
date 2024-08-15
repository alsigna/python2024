from netaddr import IPAddress, IPNetwork

net = IPNetwork("192.168.1.0/24")
print(net)


net = IPNetwork("192.168.1.100/23")
print(net)


print("адрес сети:", net.network)
print("маска сети:", net.netmask)
print("длина маски:", net.prefixlen)
print("cidr представление:", net.cidr)
print("wildcard маска:", net.hostmask)
print("broadcast адрес:", net.broadcast)
print("первый хост сети:", IPAddress(net.first))
print("последний хост сети:", IPAddress(net.last))
