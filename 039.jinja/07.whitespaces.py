from pathlib import Path

from jinja2 import Template

template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

templates = [
    Template(template_raw),
    Template(template_raw, trim_blocks=True),
    Template(template_raw, trim_blocks=True, lstrip_blocks=True),
]

for template in templates:
    print("-" * 20)
    print(
        template.render(
            name="gi0/0/1",
            vlan_id=100,
        )
    )
