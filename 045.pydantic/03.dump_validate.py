from dataclasses import dataclass
from datetime import date

from pydantic import BaseModel

raw = {
    "count": "4",
    "force": 1,
    "date": "2024-04-28",
}

# @dataclass
# class M:
#     count: int
#     force: bool
#     date: date


class M(BaseModel):
    count: int
    force: bool
    date: date


m = M.model_validate(raw)
print(m.model_dump())
