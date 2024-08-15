from netaddr import EUI, mac_cisco, mac_pgsql

mac = EUI(addr="0007.ECE1.5D18")
print(mac)
print(mac.format(dialect=mac_cisco))
print(mac.format(dialect=mac_pgsql))

mac = EUI(addr="0007.ECE1.5D18", dialect=mac_cisco)
print(mac)


class mac_huawei(mac_cisco):
    word_sep = "-"


print(mac.format(dialect=mac_huawei))
