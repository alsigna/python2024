import re
from io import StringIO

import pexpect

username = "admin"
password = "P@ssw0rd"
ip = "192.168.122.101"

password_pattern: re.Pattern = re.compile("password:", flags=re.IGNORECASE)

buffer = StringIO()

ssh = pexpect.spawn(
    command=f"ssh {username}@{ip}",
    timeout=5,
    logfile=buffer,
    encoding="utf-8",
)

r = ssh.expect([password_pattern, r"\[fingerprint\]"])
if r == 0:
    ssh.sendline(password)
    ssh.expect("#")
elif r == 1:
    ssh.sendline("yes")
    ssh.expect(password_pattern)
    ssh.sendline(password)
    ssh.expect("#")

ssh.sendline("terminal length 0")
ssh.expect("#")

ssh.sendline("show version")
ssh.expect("#")

ssh.sendline("show ip interface brief")
ssh.expect("#")

output = ssh.before
interfaces = []
for line in output.splitlines():
    m = re.search(r"(?P<name>\S+)\s+\d\S+\s+YES\s+\w+\s+up\s+up", line)
    if m is not None:
        interfaces.append(m.group("name"))

for i in interfaces:
    ssh.sendline(f"show run int {i}")
    ssh.expect("#")

ssh.sendline("exit")
ssh.expect("closed.")

with open("./046.pexpect/05.before.log", "w") as f:
    f.write(buffer.getvalue())
