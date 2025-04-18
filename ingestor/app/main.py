import uvicorn

from fastapi import FastAPI

from .config.settings import get_settings 
from .models.schemas import PulseModel

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

@app.post("/pulse/")
async def create_pulse(pulse: PulseModel):
    return get_settings()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
