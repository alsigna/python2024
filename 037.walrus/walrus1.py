text = "строка для примера"

data = {
    "words": text.split(),
    "symbols": len("".join(text.split())),
}

print(data)


text = "строка для примера"
data = {
    "words": (words := text.split()),
    "symbols": len("".join(words)),
}
print(data)

ip = "192.168.1.123/24"
octets = [
    int(ip.split("/")[0].split(".")[0]),
    int(ip.split("/")[0].split(".")[1]),
    int(ip.split("/")[0].split(".")[2]),
    int(ip.split("/")[0].split(".")[3]),
]
print(octets)


ip = "192.168.1.123/24"
octets = [
    int((ip_octets := ip.split("/")[0].split("."))[0]),
    int(ip_octets[1]),
    int(ip_octets[2]),
    int(ip_octets[3]),
]
print(octets)
