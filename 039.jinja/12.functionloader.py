from pathlib import Path
from typing import Literal

from jinja2 import Environment, FunctionLoader


def get_template(device_type: Literal["sw", "rt"]) -> str:
    """функция для чтения файлов с шаблонами в строку

    Args:
        device_type: (str): тип устройства "sw" или "rt"

    Returns:
        str: шаблон в виде строки
    """
    template_file = Path(
        Path(__file__).parent,
        "templates",
        Path(__file__).name,
    ).with_suffix(f".{device_type}.j2")
    if not template_file.is_file():
        return None
        # raise ValueError(f"шаблона {template_file} нет")
    with open(template_file, "r") as f:
        template_text = f.read()
    return template_text


# создаем FunctionLoader, передавая функцию в качестве аргумента
loader = FunctionLoader(load_func=get_template)
# загрузка шаблонов в Environment
env = Environment(loader=loader)

# входные данные для генерации конфигурации
devices = [
    {
        "type": "rt",
        "name": "rt1",
        "mgmt_ip": "192.168.1.101",
    },
    {
        "type": "sw",
        "name": "sw1",
        "mgmt_ip": "192.168.1.102",
        "access_vlan": 100,
        "if_name": "Gi1/0/1",
    },
]
# генерация конфига в зависимости от типа устройства
for device in devices:
    device_type = device["type"]
    template = env.get_template(device_type)
    config = template.render(device)
    print("-" * 10, "config of", device["name"])
    print(config)
