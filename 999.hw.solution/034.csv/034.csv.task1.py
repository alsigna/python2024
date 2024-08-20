import csv
from pathlib import Path

output = """
AP Name     AP IP             Neighbor Name        Neighbor IP      Neighbor Port
---------   ---------------   ------------------   --------------   -------------
SB_RAP1     192.168.102.154   sjc14-41a-sw1        192.168.102.2    GigabitEthernet1/0/13
SB_RAP1     192.168.102.154   SB_MAP1              192.168.102.137  Virtual-Dot11Radio0
SB_MAP1     192.168.102.137   SB_RAP1              192.168.102.154  Virtual-Dot11Radio0
SB_MAP1     192.168.102.137   SB_MAP2              192.168.102.138  Virtual-Dot11Radio0
SB_MAP2     192.168.102.138   SB_MAP1              192.168.102.137  Virtual-Dot11Radio1
SB_MAP2     192.168.102.138   SB_MAP3              192.168.102.139  Virtual-Dot11Radio0
SB_MAP3     192.168.102.139   SB_MAP2              192.168.102.138  Virtual-Dot11Radio1
""".strip()


aps: dict[str, str] = {}
for line in output.splitlines()[2:]:
    ap, ip, *_ = line.split()
    # if ap not in aps:
    aps.update({ap: ip})


to_csv = [("ap_name", "ap_ip")]
to_csv.extend(list(aps.items()))


filename = Path(__file__).parent / f"034.csv.csv"
with open(filename, "w") as f:
    writer = csv.writer(f)
    for line in to_csv:
        writer.writerow(line)
