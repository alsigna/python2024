# Дан вывод

# ```python
# output = """
# Interface             IP-Address      OK?    Method Status      Protocol
# GigabitEthernet0/2    192.168.190.235 YES    unset  up          up
# GigabitEthernet0/4    192.168.191.2   YES    unset  up          down
# TenGigabitEthernet2/1 unassigned      YES    unset  up          up
# Te36/45               unassigned      YES    unset  down        down
# """.strip()
# ```

# Создать namedtuple `InterfaceStatus` и сделать список `intf_brief = <...>` из 4ех элементов типа `InterfaceStatus`, в каждом из котором будет разобранные из соответсвующей строки входных данных (заголовок пропускаем, он не нужен, только данные по интерфейсам).

from collections import namedtuple

output = """
Interface             IP-Address      OK?    Method Status      Protocol
GigabitEthernet0/2    192.168.190.235 YES    unset  up          up
GigabitEthernet0/4    192.168.191.2   YES    unset  up          down
TenGigabitEthernet2/1 unassigned      YES    unset  up          up
Te36/45               unassigned      YES    unset  down        down
""".strip()

InterfaceStatus = namedtuple("InterfaceStatus", ["name", "ip", "ok", "method", "status", "protocol"])

_, *interfaces = output.split("\n")

intf_brief = [
    InterfaceStatus(*interfaces[0].split()),
    InterfaceStatus(*interfaces[1].split()),
    InterfaceStatus(*interfaces[2].split()),
    InterfaceStatus(*interfaces[3].split()),
]
