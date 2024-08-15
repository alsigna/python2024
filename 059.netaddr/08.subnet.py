from netaddr import IPNetwork

net = IPNetwork("192.168.1.100/23")


for subnet in net.subnet(25):
    print(repr(subnet))
