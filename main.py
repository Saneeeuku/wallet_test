import uvicorn
from fastapi import FastAPI

from config import settings as s

app = FastAPI()


@app.get("/")
async def root():
    return {"go to": f"http://{s.UVC_HOST}:{s.UVC_PORT}/docs"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=s.UVC_HOST,
        port=s.UVC_PORT,
        reload=s.UVC_RELOAD,
    )
