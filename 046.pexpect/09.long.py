import re
from io import StringIO

import pexpect


def get_show_output(username: str, password: str, enable: str, ip: str, cmd: str) -> str:
    def _get_prompt() -> str:
        ssh.sendline("")
        prompt = ssh.before.strip() + ssh.after
        ssh.expect(prompt)
        return prompt

    def _get_output() -> str:
        prompt = _get_prompt()
        output = ""
        ssh.sendline(cmd)
        while True:
            m = ssh.expect([prompt, r"\s*--More--", r"Invalid input detected"])
            page = ssh.before
            page = re.sub(r"(?:\s*\x08+)+", "\r\n", page)
            if m == 0:
                output += page
                output = re.sub(rf"^{cmd}\r\n", "", output)
                return output
            elif m == 1:
                output += page
                ssh.send(" ")
            elif m == 2 and prompt.endswith(">"):
                ssh.sendline("enable")
                ssh.expect(password_pattern)
                ssh.sendline(password)
                ssh.expect("#")
                prompt = _get_prompt()
                ssh.sendline(cmd)
            else:
                return output

    password_pattern: re.Pattern = re.compile("password:", flags=re.IGNORECASE)
    logfile = StringIO()
    with pexpect.spawn(
        command=f"ssh {username}@{ip}",
        timeout=5,
        encoding="utf-8",
        logfile=logfile,
    ) as ssh:
        m = ssh.expect([password_pattern, r"\[fingerprint\]"])
        if m == 1:
            ssh.sendline("yes")
            ssh.expect(password_pattern)
        ssh.sendline(password)
        m = ssh.expect(["#", ">"])

        output = _get_output()

    with open("./046.pexpect/09.long.log", "w") as f:
        f.write(logfile.getvalue())

    return output


if __name__ == "__main__":
    username = "admin"
    password = "P@ssw0rd"
    ip = "192.168.122.101"

    output = get_show_output(username, password, password, ip, "show runn")
    with open("./046.pexpect/09.long.txt", "w") as f:
        f.write(output)
