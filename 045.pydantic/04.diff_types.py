from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr


class IP(BaseModel):
    address: str
    mask: int


class MyModel(BaseModel):
    count: int
    force: bool
    date: date
    ip: IP
    uuid: UUID
    email: EmailStr


raw = {
    "count": "4",
    "force": 1,
    "date": "2024-04-28",
    "ip": {
        "address": "1.1.1.1",
        "mask": "24",
    },
    "uuid": "93e98c71-7042-4e65-9543-5df19ee6f03b",
    "email": "my@abcd.com",
}

m = MyModel.model_validate(raw)
