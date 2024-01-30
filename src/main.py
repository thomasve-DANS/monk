from fastapi import FastAPI

from models import (
    LogEvent,
    CompletedLogEvent
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Magic": "Begins here"}

@app.post("/log")
def create_log(data: LogEvent):
    data.log()
    return CompletedLogEvent(**dict(data))
