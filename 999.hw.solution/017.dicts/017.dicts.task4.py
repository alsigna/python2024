# Есть базовая заготовка (шаблон)

# ```python
# SCRAPLI_TEMPLATE = {
#     "auth_username": "cisco",
#     "auth_password": "password",
#     "transport": "system",
#     "auth_strict_key": False,
#     "port": 22,
# }
# ```

# Создать список из двух словарей на основе шаблона `SCRAPLI_TEMPLATE` дополнив/обновив его
# парами ключ = значение (сам шаблон при этом меняться не должен)


SCRAPLI_TEMPLATE = {
    "auth_username": "cisco",
    "auth_password": "password",
    "transport": "system",
    "auth_strict_key": False,
    "port": 22,
}


device1 = SCRAPLI_TEMPLATE | {"hostname": "sw1.abcd.net"}

device2 = SCRAPLI_TEMPLATE | {
    "hostname": "sw1.abcd.net",
    "transport": "telnet",
    "port": 23,
}
