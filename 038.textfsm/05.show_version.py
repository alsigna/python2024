from pathlib import Path
from pprint import pprint

import textfsm

output = """
r1#show version
Cisco IOS XE Software, Version 17.03.03
Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.3, RELEASE SOFTWARE (fc7)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2021 by Cisco Systems, Inc.
Compiled Thu 04-Mar-21 12:49 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON

r1 uptime is 1 hour, 5 minutes
Uptime for this control processor is 1 hour, 8 minutes
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: reload


          
This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

License Level: ax
License Type: N/A(Smart License Enabled)
Next reload license Level: ax

The current throughput level is 1000 kbps 


Smart Licensing Status: UNREGISTERED/No Licenses in Use

cisco CSR1000V (VXE) processor (revision VXE) with 2071913K/3075K bytes of memory.
Processor board ID 9TVPJOLCFIS
Router operating mode: Autonomous
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
3978412K bytes of physical memory.
6188032K bytes of virtual hard disk at bootflash:.

Configuration register is 0x2102
"""

# Value platform ([\S ]+)
# Value version (\S+)
# Value hostname (\S+)
# Value pid (\S+)
# Value sn (\S+)
# Value confreg (\S+)

# Start
#   # Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.9(3)M3, RELEASE SOFTWARE (fc1)
#   ^Cisco\s+IOS\s+Software,\s+${platform}\s+Software\s+\(\S+\), Version\s+${version},
#   # Cisco IOS XE Software, Version 17.03.03
#   ^Cisco\s+${platform}\s+Software, Version\s+${version}
#   # r1 uptime is 1 hour, 5 minutes
#   ^${hostname}\s+uptime\s+is\s+${uptime}$$
#   # cisco CSR1000V (VXE) processor (revision VXE) with 2071913K/3075K bytes of memory.
#   ^cisco\s+${pid}\s+
#   # Processor board ID 9TVPJOLCFIS
#   ^Processor\s+board\s+ID\s+${sn}
#   # Configuration register is 0x2102
#   ^Configuration\s+register\s+is\s+${confreg}

template = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")
with open(template, "r") as f:
    fsm = textfsm.TextFSM(f)


result = fsm.ParseTextToDicts(output)
pprint(result)
