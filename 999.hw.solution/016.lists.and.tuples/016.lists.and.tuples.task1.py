# Есть список

# ```python
# intf_list = ["gi0/0", "gi0/1", "gi0/22", "gi0/23", "gi0/3", "gi0/4"]
# ```

# Нужно преобразовть к вот такому виду `["gi0/0", "gi0/1", "gi0/2", "gi0/3", "gi0/4"]` (gi0/22, gi0/23 лишние элементы, gi0/2 не хватает)


# вариант1
intf_list = ["gi0/0", "gi0/1", "gi0/22", "gi0/23", "gi0/3", "gi0/4"]
intf_list.remove("gi0/22")
intf_list.remove("gi0/23")
intf_list.insert(2, "gi0/2")

# вариант2
intf_list = ["gi0/0", "gi0/1", "gi0/22", "gi0/23", "gi0/3", "gi0/4"]
intf_list[2:4] = ["gi0/2"]
