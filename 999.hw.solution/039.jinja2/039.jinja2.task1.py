from pathlib import Path

from jinja2 import Environment, FileSystemLoader

template_dir = str(Path(Path(__file__).parent, "templates"))
loader = FileSystemLoader(template_dir)

env = Environment(
    loader=loader,
    lstrip_blocks=True,
    trim_blocks=True,
    extensions=["jinja2.ext.loopcontrols"],
)

template_file = str(Path(Path(__file__).name).with_suffix(".j2"))
template = env.get_template(template_file)

interfaces = {
    "GigabitEthernet0/0/0": {
        "mtu": 1600,
        "ip": "192.168.1.1",
        "mask": "255.255.255.252",
        "type": "internal",
        "bfd": True,
    },
    "GigabitEthernet0/0/1": {
        "shutdown": True,
    },
    "GigabitEthernet0/0/2": {
        "description": "-= pe1.klg =-",
        "ip": "192.168.2.1",
        "mask": "255.255.255.252",
        "type": "external",
        "bfd": True,
    },
}
config = template.render(interfaces=interfaces)

print(config.replace("\n\n", "\n"))
