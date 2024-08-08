from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item}")
def read_item(item: int, q: str | None = None):
    return {"item": item, "q": q}
