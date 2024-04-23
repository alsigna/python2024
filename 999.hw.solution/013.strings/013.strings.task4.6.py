### Task4.6: Доработка [задания по числам](/998.hw.tasks/003.numbers.md#numbers)

# Доработать задание по числам таким образом, что бы на вход можно было подавать строку вида "ip / mask".
# В конце распечатать 5 искомых параметров (network, wildcard, broadcast, min_host_ip, max_host_ip).

ip = "192.168.43.54 / 255.255.254.0"
ip_addr, mask = ip.split(" / ")
ip_octets = ip_addr.split(".")
mask_octets = mask.split(".")

# циклы не знаем, map тоже, делаем самым простым и явным способом
net_octets = [
    int(ip_octets[0]) & int(mask_octets[0]),
    int(ip_octets[1]) & int(mask_octets[1]),
    int(ip_octets[2]) & int(mask_octets[2]),
    int(ip_octets[3]) & int(mask_octets[3]),
]

wildcard_octets = [
    255 - int(mask_octets[0]),
    255 - int(mask_octets[1]),
    255 - int(mask_octets[2]),
    255 - int(mask_octets[3]),
]

broadcast_octets = [
    int(ip_octets[0]) | wildcard_octets[0],
    int(ip_octets[1]) | wildcard_octets[1],
    int(ip_octets[2]) | wildcard_octets[2],
    int(ip_octets[3]) | wildcard_octets[3],
]


min_host = net_octets.copy()
min_host[-1] = min_host[-1] + 1

max_host = broadcast_octets.copy()
max_host[-1] = max_host[-1] - 1

print(f"network  : {net_octets[0]}.{net_octets[1]}.{net_octets[2]}.{net_octets[3]}")
print(f"wildcard : {wildcard_octets[0]}.{wildcard_octets[1]}.{wildcard_octets[2]}.{wildcard_octets[3]}")
print(f"broadcast: {broadcast_octets[0]}.{broadcast_octets[1]}.{broadcast_octets[2]}.{broadcast_octets[3]}")
print(f"min_host : {min_host[0]}.{min_host[1]}.{min_host[2]}.{min_host[3]}")
print(f"max_host : {max_host[0]}.{max_host[1]}.{max_host[2]}.{max_host[3]}")
