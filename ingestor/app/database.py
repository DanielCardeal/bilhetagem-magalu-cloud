from __future__ import annotations

from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

from app.settings import get_settings
import app.models as _ # necessário, registra os modelos do BD

_SETTINGS = get_settings()
_ENGINE = create_engine(_SETTINGS.DATABASE_URL, echo=True,
                        connect_args={"check_same_thread": False})


def _get_session() -> Generator[Session, None, None]:
    """Devolve uma sessão para manipulação do banco de dados"""
    with Session(_ENGINE) as session:
        yield session

DatabaseSession = Annotated[Session, Depends(_get_session)]

def init_db():
    SQLModel.metadata.create_all(_ENGINE)
