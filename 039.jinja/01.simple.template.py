from pathlib import Path

# импортируем Template из библиотеки jinja2
from jinja2 import Template

# читаем файл в шаблоном, можно просто писать путь
# with open("./templates/01.simple.template.j2", "r") as f:
#     template_raw = f.read()

# но в примерах будет использоваться шаблонная конструкция получения имени шаблона
template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".j2")
with open(template_file, "r") as f:
    template_raw = f.read()

# создаем экземпляр класса Template на основе прочитанного шаблона
template = Template(template_raw)

# получаем итоговую конфигурацию, методом render(), передавая в неё значения переменных
config1 = template.render(
    hostname="rt-01-dc",
    mgmt_ip="10.255.255.101",
)

# значения переменных можно заранее подготовить в словарь
rt02 = {
    "hostname": "rt-02-dc",
    "mgmt_ip": "10.255.255.102",
}
# тогда в метод render() можно передавать словарь с переменными, а не каждую переменную отдельно
config2 = template.render(rt02)

print("-" * 10)
print(config1)
print("-" * 10)
print(config2)
print("-" * 10)
