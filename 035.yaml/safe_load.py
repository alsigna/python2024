import yaml

with open("malicious.yaml", "r") as f:
    data = yaml.unsafe_load(f)


print(data)
