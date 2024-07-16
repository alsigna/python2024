from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class IP(BaseModel):
    address: IPv4Address
    mask: int = Field(ge=0, le=32, default=24)
    uuid: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)


raw = {
    "address": "1.1.1.1",
    "mask": 32,
}
ip = IP.model_validate(raw)
