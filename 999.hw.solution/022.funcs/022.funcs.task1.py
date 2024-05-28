mac_list = [
    "50-46-5D-6E-8C-20",
    "50-46-5d-6e-8c-20",
    "50:46:5d:6e:8c:20",
    "5046:5d6e:8c20",
    "50465d6e8c20",
    "50465d:6e8c20",
]


def get_mac_notation(mac):
    if len(mac.split("-")) == 6 and mac.isupper():
        notation = "IEEE EUI-48"
    elif len(mac.split("-")) == 6 and mac.islower():
        notation = "IEEE EUI-48 lowercase"
    elif len(mac.split(":")) == 6:
        notation = "UNIX"
    elif len(mac.split(":")) == 3:
        notation = "cisco"
    elif mac.isalnum():
        notation = "bare"
    else:
        notation = "неизвестна"
    return notation


for mac in mac_list:
    notation = get_mac_notation(mac)
    print(f"нотация для {mac}: {notation}")
