from pprint import pprint

from textfsm.clitable import CliTable

output = """
r2#sh cdp ne
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
r3               Gig 0/0           168              R B             Gig 0/1
r3               Gig 0/1           163              R B             Gig 0/0
r1               Gig 0/2           158              R I   CSR1000V  Gig 2
r1               Gig 0/3           158              R I   CSR1000V  Gig 1
""".strip()


cli_table = CliTable(
    index_file="index",
    template_dir="./templates",
)
attributes = {
    "Command": "sh cdp ne",
    "Platform": "cisco_ios",
}
cli_table.ParseCmd(
    cmd_input=output,
    attributes=attributes,
)

# список словарей
list_of_dict = []
for row in cli_table:
    list_of_dict.append(dict(row.items()))
# pprint(list_of_dict)

# словарь словарей
# pprint({row.get("local_interface"): dict(row.items()) for row in cli_table})
dict_of_dict = {}
for row in cli_table:
    dict_of_dict[row.get("local_interface")] = dict(row.items())
pprint(dict_of_dict)
