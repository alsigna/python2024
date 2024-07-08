from pathlib import Path
from pprint import pprint

import textfsm

output = """
Huawei Versatile Routing Platform Software
VRP (R) software, Version 5.170 (S5731 V200R021C10SPC600)
Copyright (C) 2000-2022 HUAWEI TECH Co., Ltd.
HUAWEI S5731-S48P4X Routing Switch uptime is 2 weeks, 2 days, 19 hours, 46 minutes

ES5D2V52C013 1(Master)  : uptime is 2 weeks, 2 days, 19 hours, 45 minutes
DDR             Memory Size : 2048  M bytes
FLASH Total     Memory Size : 1024  M bytes
FLASH Available Memory Size : 739   M bytes
Pcb           Version   : VER.A
MAB           Version   : 0
BootROM       Version   : 0000.0527
BootLoad      Version   : 0215.0000
CPLD          Version   : 0103
MCU           Version   : 1.14.0.12
Software      Version   : VRP (R) Software, Version 5.170 (V200R021C10SPC600)
FLASH         Version   : 0000.0000
PWR1 information
Pcb           Version   : PWR VER.B
FAN1 information
Pcb           Version   : NA
FAN2 information
Pcb           Version   : NA

ES5D2V52C013 2(Standby)  : uptime is 2 weeks, 2 days, 19 hours, 44 minutes
DDR             Memory Size : 2048  M bytes
FLASH Total     Memory Size : 1024  M bytes
FLASH Available Memory Size : 739   M bytes
Pcb           Version   : VER.A
MAB           Version   : 0
BootROM       Version   : 0000.0527
BootLoad      Version   : 0215.0000
CPLD          Version   : 0103
MCU           Version   : 1.14.0.12
Software      Version   : VRP (R) Software, Version 5.170 (V200R021C10SPC600)
FLASH         Version   : 0000.0000
PWR2 information
Pcb           Version   : PWR VER.A
FAN1 information
Pcb           Version   : NA
FAN2 information
Pcb           Version   : NA

ES5D2V52C013 3(Slave)  : uptime is 2 weeks, 2 days, 19 hours, 44 minutes
DDR             Memory Size : 2048  M bytes
FLASH Total     Memory Size : 1024  M bytes
FLASH Available Memory Size : 739   M bytes
Pcb           Version   : VER.A
MAB           Version   : 0
BootROM       Version   : 0000.0527
BootLoad      Version   : 0215.0000
CPLD          Version   : 0103
MCU           Version   : 1.14.0.12
Software      Version   : VRP (R) Software, Version 5.170 (V200R021C10SPC600)
FLASH         Version   : 0000.0000
PWR2 information
Pcb           Version   : PWR VER.B
FAN1 information
Pcb           Version   : NA
FAN2 information
Pcb           Version   : NA

ES5D2V52C013 4(Slave)  : uptime is 2 weeks, 2 days, 19 hours, 44 minutes
DDR             Memory Size : 2048  M bytes
FLASH Total     Memory Size : 1024  M bytes
FLASH Available Memory Size : 739   M bytes
Pcb           Version   : VER.A
MAB           Version   : 0
BootROM       Version   : 0000.0527
BootLoad      Version   : 0215.0000
CPLD          Version   : 0103
MCU           Version   : 1.14.0.12
Software      Version   : VRP (R) Software, Version 5.170 (V200R021C10SPC600)
FLASH         Version   : 0000.0000
PWR2 information
Pcb           Version   : PWR VER.A
FAN1 information
Pcb           Version   : NA
FAN2 information
Pcb           Version   : NA
""".strip()


template_file = Path(Path(__file__).parent, "templates", Path(__file__).name).with_suffix(".textfsm")

with open(template_file, "r") as _file:
    fsm = textfsm.TextFSM(_file)

result = fsm.ParseTextToDicts(output)
pprint(result)
