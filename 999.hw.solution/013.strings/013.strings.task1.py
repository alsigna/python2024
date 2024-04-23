from textwrap import dedent

## Task1: Многострочный текст
# Записать текст конфигурации в переменную `config`.

### Task1.1: Переменная определелена глобально

config = """
bridge-domain 555
 vlan 555 access-port interface 10GE1/0/1 to 10GE1/0/48
 vxlan vni 10555
 #
 evpn
  route-distinguisher 192.168.43.34:10555
  vpn-target 64512:10555 export-extcommunity
  vpn-target 64512:10555 import-extcommunity
 arp broadcast-suppress enable
#
""".lstrip()
# lstrip() для того, что бы убрать перенос строки в начале конфигурации

### Task1.2: Переменная определена внутри блока

if True:
    config = dedent(
        """
        bridge-domain 555
         vlan 555 access-port interface 10GE1/0/1 to 10GE1/0/48
         vxlan vni 10555
         #
         evpn
          route-distinguisher 192.168.43.34:10555
          vpn-target 64512:10555 export-extcommunity
          vpn-target 64512:10555 import-extcommunity
         arp broadcast-suppress enable
        #
        """
    ).lstrip()
    # lstrip() для того, что бы убрать перенос строки в начале конфигурации
