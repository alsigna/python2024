ip = "120.3.2.1"

first_octet = int(ip.split(".")[0])

###
# opt 1
###
first_octet_bin = f"{first_octet:08b}"

if first_octet_bin.startswith("0"):
    ip_class = "A"
elif first_octet_bin.startswith("10"):
    ip_class = "B"
elif first_octet_bin.startswith("110"):
    ip_class = "C"
elif first_octet_bin.startswith("1110"):
    ip_class = "D"
elif first_octet_bin.startswith("1111"):
    ip_class = "E"
else:
    ip_class = "unknown"

print(f"класс ip {ip}: {ip_class}")

###
# opt 2
###
if first_octet < 128:
    ip_class = "A"
elif 128 <= first_octet < 192:
    ip_class = "B"
elif 192 <= first_octet < 224:
    ip_class = "C"
elif 224 <= first_octet < 240:
    ip_class = "D"
elif 240 <= first_octet < 256:
    ip_class = "E"
else:
    ip_class = "unknown"

print(f"класс ip {ip}: {ip_class}")

###
# opt 3
###
ip_classes = {
    "A": range(128),
    "B": range(128, 192),
    "C": range(192, 224),
    "D": range(224, 240),
    "E": range(240, 256),
}
ip_class = "unknown"
for class_, range_ in ip_classes.items():
    if first_octet in range_:
        ip_class = class_

print(f"класс ip {ip}: {ip_class}")
