from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# задаем имя каталога, где находятся шаблоны (в примере добавляем ./templates к каталогу, в котором
# находится запускаемый py файл)
template_dir = str(Path(Path(__file__).parent, "templates"))
# определям способ получения шаблонов, в простом варианте это FileSystemLoader,
# т.е. шаблоны будут читаться с диска, из каталога определенного в template_dir
loader = FileSystemLoader(template_dir)

# создаем экземпляр класса Environment и передаем в качестве аргумента способ получения шаблонов
env = Environment(loader=loader)

# определяем имя шаблона, просто меняем расширение py на j2 у имени запускаемого py файла
template_file = str(Path(Path(__file__).name).with_suffix(".j2"))
# получаем сам шаблон, указав его имя
template = env.get_template(template_file)

# получаеи итоговый текст методом render(), передавая в него значения переменных (можно и через словарь)
config = template.render(
    hostname="rt-02-dc",
    mgmt_ip="10.255.255.102",
)

print(config)
