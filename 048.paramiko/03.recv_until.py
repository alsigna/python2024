import time

import paramiko


def get_show_output(username: str, password: str, enable: str, ip: str, cmd: str) -> str:
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=ip,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
        )
        with client.invoke_shell() as ssh:
            ssh.send("term len 0\n")
            time.sleep(1)
            prompt = ssh.recv(10000)
            prompt = prompt.split()[-1].decode()
            if prompt.endswith(">"):
                ssh.send("enable\n")
                time.sleep(1)
                ssh.send(enable + "\n")
                time.sleep(1)
            prompt = ssh.recv(10000)
            # print(f"{prompt=}")
            prompt = prompt.split()[-1].decode()
            # print(f"{prompt=}")

            ssh.send(cmd + "\n")
            result = ""
            while True:
                time.sleep(0.2)
                result += ssh.recv(1000).decode()
                if result.endswith(prompt):
                    return result


output = get_show_output("admin", "P@ssw0rd", "P@ssw0rd", "192.168.122.101", "show run")
print(output)
