from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

template = Template(template_raw)

data = {
    "name": "rt01-msk",
    "vlans": [101, 102, 103],
    "ospf": {
        "rid": "10.255.255.1",
        "area": {"a": "b"},
    },
}

config = template.render(data)

print(config)
