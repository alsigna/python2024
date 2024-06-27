from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

template = Template(template_raw)

interfaces = {
    "gi0/0/1": {
        "description": "primary interface",
        "ip": "10.0.0.1",
        "mask": "255.255.255.252",
    },
    "gi0/0/2": {
        "description": "backup interface",
        "ip": "10.0.1.1",
        "mask": "255.255.255.252",
    },
}


config = template.render(interfaces=interfaces)

print(config)


# template_loop = """
# {% for vlan in vlans %}
# vlanid: {{ vlan }}, текущая итерация цикла {{ loop.index }}, имя vlan: {{ names[loop.index0]}}
# {% endfor %}
# """.strip()

# template = Template(template_loop)
# print(
#     template.render(
#         vlans=[101, 102, 103, 104, 105],
#         names=["voip", "user", "server", "mgmt", "wifi"],
#     )
# )


# template_changed = """
# {% for name, data in peers.items() %}
# {% if loop.changed(name) %}
# !
# {% endif %}
#   {% for config in data %}
# peer {{ name }} {{ config }}
#   {% endfor %}
# {% endfor %}
# """.strip()

# template = Template(template_changed)
# print(
#     template.render(
#         peers={
#             "192.168.1.1": [
#                 "remote-as 12345",
#                 "description some peer",
#                 "allowas-in",
#             ],
#             "192.168.1.2": [
#                 "remote-as 11111",
#                 "shutdown",
#             ],
#             "192.168.1.3": [
#                 "remote-as 12345",
#             ],
#         }
#     )
# )
