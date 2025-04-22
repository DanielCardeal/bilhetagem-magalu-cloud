from contextlib import asynccontextmanager
from functools import lru_cache
import logging
from typing import Annotated, Sequence
import uvicorn

from fastapi import Depends, FastAPI

from app.aggregators import PulseAggregator, pandas_pulse_aggregator
from app.settings import Settings
from app.schemas import PulseCreate
from app.database.adapters.base import BaseDatabaseAdapter
from app.data import AggregateData
from app.database.adapters.sqlite import SQLiteDatabaseAdapter


LOG = logging.getLogger(__name__)

# Dependências


@lru_cache
def get_settings() -> Settings:
    """Devolve o objeto de configurações da aplicação."""
    return Settings()


SettingsDependency = Annotated[Settings, Depends(get_settings)]


def get_database_adapter(settings: SettingsDependency) -> BaseDatabaseAdapter:
    """Devolve uma instância do DatabaseAdapter padrão usado pela aplicação."""
    return SQLiteDatabaseAdapter(settings)


DatabaseAdapterDependency = Annotated[
    BaseDatabaseAdapter, Depends(get_database_adapter)
]


def get_pulse_aggregator() -> PulseAggregator:
    """Devolve a função agregadora de pulsos padrão usada pela aplicação."""
    return pandas_pulse_aggregator


PulseAggregatorDependency = Annotated[
    BaseDatabaseAdapter, Depends(get_pulse_aggregator)
]

# Eventos


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    # Startup
    settings = app.dependency_overrides.get(get_settings, get_settings)()

    app.title = settings.PROJECT_NAME
    app.version = settings.VERSION
    LOG.debug(f"INICIALIZANDO {settings.PROJECT_NAME} v{settings.VERSION}")
    LOG.debug(f"UVICORN VERSION {uvicorn.Config.asgi_version}")

    db_adapter: BaseDatabaseAdapter = app.dependency_overrides.get(
        get_database_adapter, get_database_adapter
    )(settings)
    db_adapter.connect()
    yield
    # Shutdown
    db_adapter.disconnect()


app = FastAPI(lifespan=lifespan_handler)


# Endpoints


@app.post("/pulse")
async def create_pulse(db_adapter: DatabaseAdapterDependency, pulse_in: PulseCreate):
    create_ok = db_adapter.create_pulse(
        tenant=pulse_in.tenant,
        product_sku=pulse_in.product_sku,
        use_unity=pulse_in.use_unity,
        used_amount=pulse_in.used_amount,
    )
    if create_ok:
        return pulse_in
    else:
        return "Failed to create pulse."


@app.get("/pulse")
async def get_aggregates(
    db_adapter: DatabaseAdapterDependency,
    aggregator: PulseAggregator = pandas_pulse_aggregator,
) -> Sequence[AggregateData]:
    pulses = db_adapter.get_pulses()
    return list(aggregator(pulses))


def app_start() -> None:
    settings = get_settings()
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)


if __name__ == "__main__":
    app_start()
