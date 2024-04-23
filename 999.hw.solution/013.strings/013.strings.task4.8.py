### Task4.8: Нормализация имен интерфейсов
# Даны имена интерфейсов в коротком виде (Eth0/1, GE1/0/2, Тen4/3). Произвести преобразование коротких имен в полные
# - Eth0/1 -> Ethernet0/1
# - GE1/0/2 -> GigabitEthernet1/0/2
# - Тen4/3 -> TenGigabitEthernet4/3

if_name1 = "Eth0/1"
if_name2 = "GE1/0/2"
if_name3 = "Ten4/3"

if_name1 = if_name1.replace("Eth", "Ethernet")
if_name2 = if_name2.replace("GE", "GigabitEthernet")
if_name3 = if_name3.replace("Ten", "TenGigabitEthernet")
