import re

s = "GigabitEthernet0/1    192.168.100.123   YES    unset  up         up"

print("при совпадении возвращается объект re.Match:")
print(re.search(r"\S+ + (?P<ip>(?:\d+\.?){4}) +\w+ + \w+ +(\w+) +(\w+)", s))

print()

print("при отсутсвия совпадения возвращается None:")
print(re.search(r"\S+ + (?P<ip>(?:\d+\.?){4}) +\w+ + \d+ +(\w+) +(\w+)", s))
