from collections import namedtuple

access = """
interface {if_name}
   switchport mode access
   switchport access vlan {vlan}
!
""".strip()

trunk = """
interface {if_name}
   switchport mode trunk
   switchport trunk allowed vlan {vlan}
!
""".strip()

intf1 = {
    "if_name": "gi0/1",
    "vlan": 102,
    "mode": "access",
}

intf2 = {
    "if_name": "gi0/2",
    "vlan": 103,
    "mode": "trunk",
}

###
# with if
###
mode = intf1.get("mode")
if mode == "access":
    intf1_config = access.format(**intf1)
elif mode == "trunk":
    intf1_config = trunk.format(**intf1)
else:
    intf1_config = "unknown mode"

mode = intf2.get("mode")
if mode == "access":
    intf2_config = access.format(**intf2)
elif mode == "trunk":
    intf2_config = trunk.format(**intf2)
else:
    intf2_config = "unknown mode"

print("-" * 10, "with if", "-" * 10)
print(intf1_config)
print(intf2_config)


###
# w/o if
###
templates = {
    "access": access,
    "trunk": trunk,
}

intf_template = templates.get(intf1.get("mode"), "")
intf1_config = intf_template.format(**intf1)

intf_template = templates.get(intf2.get("mode"), "")
intf2_config = intf_template.format(**intf2)

print("\n" * 2 + "-" * 10, "without if", "-" * 10)
print(intf1_config)
print(intf2_config)

###
# other example
###
signs = {"succeeded": "\u2705", "failed": "\u274C", "skipped": "\u2757"}
Task = namedtuple("Task", ("hostname", "status", "message"))
tasks = [
    Task("r1", "succeeded", "upgrade completed"),
    Task("r2", "failed", "not enough space on disk"),
    Task("r3", "skipped", "device is not reachable"),
]

print("\n" * 2 + "-" * 10, "other example", "-" * 10)
for task in tasks:
    print(f"{task.hostname}: {signs.get(task.status)} {task.message}")
