from pydantic import BaseModel


class IP(BaseModel):
    address: str
    mask: int = 24


raw = {
    "address": "1.1.1.1",
}

ip = IP.model_validate(raw)
