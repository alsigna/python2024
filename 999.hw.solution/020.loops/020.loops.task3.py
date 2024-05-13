from pprint import pprint

SCRAPLI_TEMPLATE = {
    "auth_username": "cisco",
    "auth_password": "password",
    "transport": "system",
    "auth_strict_key": False,
    "port": 22,
}

hostnames = ["rt1", "rt2", "sw1", "sw2"]

###
# with for
###
devices = {}
for hostname in hostnames:
    devices[hostname] = SCRAPLI_TEMPLATE | {"hostname": hostname}

print("-" * 10, "with for", "-" * 10)
pprint(devices)

###
# with dict comprehension
###
devices = {hostname: SCRAPLI_TEMPLATE | {"hostname": hostname} for hostname in hostnames}
print("\n" * 2 + "-" * 10, "with dict comprehension", "-" * 10)
pprint(devices)
