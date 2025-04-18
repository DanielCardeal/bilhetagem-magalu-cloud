from typing import Sequence
from sqlmodel import select
import uvicorn

from fastapi import FastAPI

from app.settings import get_settings
from app.models import Pulse, PulseCreate
from app.database import DatabaseSession, init_db

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/pulse/")
async def create_pulse(session: DatabaseSession, pulse_in: PulseCreate) -> Pulse:
    db_pulse = Pulse.model_validate(pulse_in)
    session.add(db_pulse)
    session.commit()
    session.refresh(db_pulse)
    return db_pulse


@app.get("/pulse/")
async def get_pulses(session: DatabaseSession) -> Sequence[Pulse]:
    pulses = session.exec(select(Pulse)).all()
    return pulses

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
