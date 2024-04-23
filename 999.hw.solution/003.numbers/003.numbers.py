ip1, ip2, ip3, ip4 = 192, 168, 43, 54
m1, m2, m3, m4 = 255, 255, 255, 240

net1 = ip1 & m1
net2 = ip2 & m2
net3 = ip3 & m3
net4 = ip4 & m4
print("network  :", net1, net2, net3, net4)

wcm1, wcm2, wcm3, wcm4 = 255 - m1, 255 - m2, 255 - m3, 255 - m4
print("wildcard :", wcm1, wcm2, wcm3, wcm4)

bc1, bc2, bc3, bc4 = ip1 | wcm1, ip2 | wcm2, ip3 | wcm3, ip4 | wcm4
print("broadcast:", bc1, bc2, bc3, bc4)

print("min_host :", net1, net2, net3, net4 + 1)
print("max_host :", bc1, bc2, bc3, bc4 - 1)


# читаемость имеет значимость, если умеете/знаете циклы/map/zip/etc то можно добавить,
# что бы каждый отктет не расписывать. Но точно не нужно что-то типа такого делать. В
# данном случае лучше лишние строки кода, чем сильная вложенность функций
ip = "192.168.53.123 / 255.255.255.240"
network = ".".join(map(str, [int(i) & int(m) for i, m in zip(*[o.split(".") for o in ip.split(" / ")])]))
wildcart = ".".join(map(str, [255 - int(m) for _, m in zip(*[o.split(".") for o in ip.split(" / ")])]))

print("-" * 10)
print("network  :", network)
print("wildcard :", wildcart)
