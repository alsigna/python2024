from netmiko import SSHDetect

params = {
    "device_type": "autodetect",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}

detect = SSHDetect(**params)
platform = detect.autodetect()

print(platform)
