import time
from random import randint

from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item}")
def read_item(item: int):
    delay = randint(50, 300) / 100
    time.sleep(delay)
    return {"item": item, "delay": delay}
