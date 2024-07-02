from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

template = Template(
    template_raw,
    lstrip_blocks=True,
    trim_blocks=True,
)

interfaces = {
    "gi0/0/1": {
        "description": "PEER SW",
        "vlans": [101, 102, 103],
    },
    "gi0/0/2": {
        "vlans": 102,
    },
}

config = template.render(interfaces=interfaces)

print(config.replace("\n\n", "\n"))
