from pprint import pprint

from textfsm.clitable import CliTable

output = """
sw2# show interface counters errors

--------------------------------------------------------------------------------
Port          Align-Err    FCS-Err   Xmit-Err    Rcv-Err  UnderSize OutDiscards
--------------------------------------------------------------------------------
Eth1/1                61         0          0          0          0           0
Eth1/2                62         0          0          0          0           0
Eth1/3                63         0          0          0          0           0
Eth1/4                64         0          0          0          0           0
Eth1/5                65         0          0          0          0           0

--------------------------------------------------------------------------------
Port         Single-Col  Multi-Col   Late-Col  Exces-Col  Carri-Sen       Runts
--------------------------------------------------------------------------------
Eth1/1                21         0          0          0          0           0
Eth1/2                22         0          0          0          0           0
Eth1/3                23         0          0          0          0           0
Eth1/4                24         0          0          0          0           0
Eth1/5                25         0          0          0          0           0

--------------------------------------------------------------------------------
Port          Giants SQETest-Err Deferred-Tx IntMacTx-Er IntMacRx-Er Symbol-Err
--------------------------------------------------------------------------------
Eth1/1             31         --           0           0           0          0
Eth1/2             32         --           0           0           0          0
Eth1/3             33         --           0           0           0          0
Eth1/4             34         --           0           0           0          0
Eth1/5             35         --           0           0           0          0

--------------------------------------------------------------------------------
Port         InDiscards
--------------------------------------------------------------------------------
Eth1/1                41
Eth1/2                42
Eth1/3                43
Eth1/4                44
Eth1/5                45
""".strip()


cli_table = CliTable(
    index_file="index",
    template_dir="./templates",
)
attributes = {
    "Command": "sh inter coun err",
    "Platform": "cisco_nxos",
}
cli_table.ParseCmd(
    cmd_input=output,
    attributes=attributes,
)


pprint({row.get("Interface"): dict(row.items()) for row in cli_table})
