from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

template = Template(template_raw, lstrip_blocks=True, trim_blocks=True)

data = {
    "vlans": {
        101: "user",
        102: "voip",
        103: "server",
        104: "mgmt",
    },
    "trunks": [
        "gi0/0/1",
        "gi0/0/2",
    ],
}

config = template.render(data)

print(config)
