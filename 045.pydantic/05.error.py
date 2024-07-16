from pydantic import BaseModel


class IP(BaseModel):
    address: str
    mask: int


raw = {
    "address": "1.1.1.1",
}

ip = IP.model_validate(raw)


raw = {
    "address": "1.1.1.1",
    "mask": "255.255.255.0",
}
ip = IP.model_validate(raw)
