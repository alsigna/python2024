from netaddr import IPAddress, ipv6_compact, ipv6_full, ipv6_verbose

ipv4 = IPAddress("192.168.1.1")
ipv6 = IPAddress("2001:C0FE:ABCD:12::1")

print(str(ipv4))

print("строка по умолчанию:", str(ipv6))
print("ipv6_compact:", ipv6.format(ipv6_compact))
print("ipv6_full:", ipv6.format(ipv6_full))
print("ipv6_verbose:", ipv6.format(ipv6_verbose))
