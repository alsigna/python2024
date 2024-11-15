import paramiko

with open("/Users/alexigna/.ssh/gcp_eve_rsa", "r") as f:
    privkey = paramiko.RSAKey.from_private_key(f)

with paramiko.SSHClient() as client:
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname="34.34.190.10",
        username="alexigna",
        pkey=privkey,
    )
    client.exec_command("rm python.example")
    stdin, stdout, stderr = client.exec_command("ls -la")
    stdin.close()

    if not stderr.readlines():
        res = stdout.read().decode()
    else:
        res = ""


print(res)
