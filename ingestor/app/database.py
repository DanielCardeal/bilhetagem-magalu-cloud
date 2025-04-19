from __future__ import annotations

from typing import Generator
from sqlmodel import create_engine, SQLModel, Session

from app.settings import Settings
import app.models as _  # necessário, registra os modelos do BD

class DBSessionManager:
    _instance = None
    _engine = None
    _settings = None

    def __new__(cls, settings: Settings) -> DBSessionManager:
        if cls._instance is None:
            cls._instance = super(DBSessionManager, cls).__new__(cls)
            cls._settings = settings
            cls._engine = create_engine(
                cls._settings.DATABASE_URL, 
                echo=True,
                connect_args={"check_same_thread": False}
            )
        return cls._instance

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise ValueError("Database engine not initialized")
        return cls._engine

    @classmethod
    def generate_db_session(cls) -> Generator[Session, None, None]:
        with Session(cls.get_engine()) as session:
            yield session

    @classmethod
    def init_db(cls):
        SQLModel.metadata.create_all(cls.get_engine())
