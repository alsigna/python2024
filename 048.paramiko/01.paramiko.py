import time

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    hostname="192.168.122.101",
    port=22,
    username="admin",
    password="P@ssw0rd",
    look_for_keys=False,
    allow_agent=False,
    timeout=5,
)
ssh = client.invoke_shell()
ssh.send("show ip interface brief\n")
time.sleep(2)
result = ssh.recv(10000)
ssh.close()

print(result.decode())
