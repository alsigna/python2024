## Task4: Форматирование строк

### Task4.1: Простейший шаблон
# Сделать из текста
# шаблон со следующими входными параметрами (название переменной / описание / пример значения в шаблоне)
# - `bd_id` / bridge domain id / 555
# - `intf_start` / первый интерфейс / 10GE1/0/1
# - `intf_end` / последний интерфейс / 10GE1/0/48
# - `rid` / router id / 192.168.43.34
# - `bgp_as` / номер bgp as / 64512


template = """
#
bridge-domain {bd_id}
 vlan {bd_id} access-port interface {intf_start} to {intf_end}
 vxlan vni 1{bd_id:04}
 #
 evpn
  route-distinguisher {rid}:1{bd_id:04}
  vpn-target {bgp_as}:1{bd_id:04} export-extcommunity
  vpn-target {bgp_as}:1{bd_id:04} import-extcommunity
 arp broadcast-suppress enable
#
""".lstrip()

# Восстановить исходный текст из шаблона, передав в него необходимые параметры:
config1 = template.format(
    bd_id=555,
    intf_start="10GE1/0/1",
    intf_end="10GE1/0/48",
    rid="192.168.43.34",
    bgp_as=64512,
)

# Получить конфигурацию для еще двух наборов параметров (меняем только `bd_id`, остальные можно оставить без изменений)
# и убедиться, что rd/rt/vni формируются без ошибок
# - `bd_id` = 2541. Ожидаем в vni/rt/rf - 12541
# - `bd_id` = 84. Ожидаем в vni/rt/rf - 10084

config2 = template.format(
    bd_id=2541,
    intf_start="10GE1/0/1",
    intf_end="10GE1/0/48",
    rid="192.168.43.34",
    bgp_as=64512,
)
config3 = template.format(
    bd_id=84,
    intf_start="10GE1/0/1",
    intf_end="10GE1/0/48",
    rid="192.168.43.34",
    bgp_as=64512,
)
