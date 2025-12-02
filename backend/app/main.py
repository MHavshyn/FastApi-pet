import socket

from fastapi import FastAPI

app = FastAPI(
    root_path="/api",
)

@app.get("/info")
async def get_backend():
    return {"backend": socket.gethostname()}


