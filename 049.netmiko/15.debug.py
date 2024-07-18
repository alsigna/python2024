import logging

import netmiko

logger = logging.getLogger("netmiko")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
logger.addHandler(sh)

fh = logging.FileHandler("./049.netmiko/15.debug.log")
logger.addHandler(fh)


params = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}
with netmiko.ConnectHandler(**params) as ssh:
    ssh.enable()
    output = ssh.save_config()

print(output)
