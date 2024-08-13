import asyncio
from random import randint

from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/items/{item}")
async def read_item(item: int):
    delay = randint(50, 300) / 100
    await asyncio.sleep(delay)
    return {"item": item, "delay": delay}
