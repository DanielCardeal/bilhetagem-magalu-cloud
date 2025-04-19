import logging
from typing import Annotated, Sequence
from sqlmodel import select, Session
import uvicorn

from fastapi import Depends, FastAPI
from app.aggregator import PulseAggregator, pandas_pulse_aggregator

from app.settings import Settings
from app.models import Pulse, PulseAggregate, PulseCreate
from app.database import DBSessionManager


SETTINGS = Settings()
LOG = logging.getLogger(__name__)

DatabaseSessionDependency = Annotated[Session, Depends(DBSessionManager.generate_db_session)]

app = FastAPI(
    title=SETTINGS.PROJECT_NAME,
    version=SETTINGS.VERSION,
)

@app.on_event("startup")
def on_startup():
    DBSessionManager.init_db()


@app.post("/pulse/")
async def create_pulse(session: DatabaseSessionDependency, pulse_in: PulseCreate) -> Pulse:
    db_pulse = Pulse.model_validate(pulse_in)
    session.add(db_pulse)
    session.commit()
    session.refresh(db_pulse)
    return db_pulse


@app.get("/pulse")
async def get_aggregates(
        session: DatabaseSessionDependency,
        aggregator: PulseAggregator = pandas_pulse_aggregator
) -> Sequence[PulseAggregate]:
    pulses = session.exec(select(Pulse)).all()
    return list(aggregator(pulses))

def app_start() -> None:
    LOG.info(f"Inicializando serviço {SETTINGS.PROJECT_NAME}")
    LOG.info(uvicorn.Config.asgi_version)
    DBSessionManager(SETTINGS)
    uvicorn.run(app, host=SETTINGS.SERVER_HOST, port=SETTINGS.SERVER_PORT)

if __name__ == "__main__":
    app_start()
