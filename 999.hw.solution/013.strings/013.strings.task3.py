## Task3: Работа с байтовой последовательностью

### Task3.1: Преобразование в utf-8
# С оборудования получили следующий вывод, нужно преобразовать его в unicode (utf-8) строку.

output = b"""\r\nHuawei Versatile Routing Platform Software\r\nVRP (R) software, Version 8.220 (CE6857EI V200R022C00SPC500)\r\nCopyright (C) 2012-2022 Huawei Technologies Co., Ltd.\r\nHUAWEI CE6857-48S6CQ-EI uptime is 248 days, 3 hours, 14 minutes\r\n"""

# utf-8 является целевой кодировкой по умолчанию, можно не указывать, а можно явно прописать, ошибки нет
output = output.decode()

### Task3.2: Возврат каретки (CR)
# У полученной в Task3.1 строки избавится от символа возврата каретки.

output = output.replace("\r", "")

### Task3.3: Пробельные символы
# У полученной в Task3.2 строки удалить пробельные символы только с начала строки.

output = output.lstrip()
