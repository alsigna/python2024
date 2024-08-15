import ipaddress

net = ipaddress.IPv4Network("192.168.1.100/23", strict=False)


for subnet in net.subnets(new_prefix=25):
    print(repr(subnet))
