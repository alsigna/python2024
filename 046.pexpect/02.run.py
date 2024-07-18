import io

import pexpect

buffer = io.StringIO()

result = pexpect.run(
    command="telnet 192.168.122.101",
    events={
        "(?i)username:": "admin\n",  # (?i) - без учета регистра https://docs.python.org/3/library/re.html#regular-expression-syntax
        "(?i)password:": "P@ssw0rd\n",
        "#": "show version\n",
    },
    timeout=5,
    logfile=buffer,
    encoding="utf-8",
)

print(buffer.getvalue())
