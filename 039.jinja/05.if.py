from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

template = Template(template_raw)

interfaces = {
    "gi0/0/1": {"action": "remove", "vlan_id": 101},
    "gi0/0/2": {"action": "override", "vlan_id": 102},
    "gi0/0/3": {"action": "", "vlan_id": 103},
}

config = template.render(interfaces=interfaces)

print(config)
