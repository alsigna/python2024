seq = ["rt1", "RT2", "SW1", "sw2"]

print(list(filter(lambda x: x.lower().startswith("rt"), seq)))
