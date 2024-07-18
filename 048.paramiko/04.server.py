import paramiko

with open("/Users/alexigna/.ssh/gcp_eve_rsa", "r") as f:
    privkey = paramiko.RSAKey.from_private_key(f)

with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname="34.140.213.179",
        username="alexigna",
        pkey=privkey,
    )
    # ssh.exec_command("rm python.exaple")
    stdin, stdout, stderr = ssh.exec_command("ls -la")
    stdin.close()

    if not stderr.readlines():
        res = stdout.read().decode()
    else:
        res = ""


print(res)
