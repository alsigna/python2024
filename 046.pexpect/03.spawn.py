import re

import pexpect

username = "admin"
password = "P@ssw0rd"
ip = "192.168.122.101"

password_pattern: re.Pattern = re.compile("password:", flags=re.IGNORECASE)

with open("./046.pexpect/03.spawn.log", "w") as f:
    ssh = pexpect.spawn(
        command=f"ssh {username}@{ip}",
        timeout=5,
        logfile=f,
        encoding="utf-8",
    )

    ssh.expect(password_pattern)
    ssh.sendline(password)
    ssh.expect("#")

    ssh.sendline("terminal length 0")
    ssh.expect("#")

    ssh.sendline("show version")
    ssh.expect("#")

    ssh.sendline("exit")
    ssh.expect("closed.")
