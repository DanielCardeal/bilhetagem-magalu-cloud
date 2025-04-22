from typing import Sequence
from sqlmodel import create_engine, SQLModel, Session, select

from app.settings import Settings
from app.database.adapters.base import BaseDatabaseAdapter
from app.database.models.sqlite import PulseModel
from app.data import PulseData


class SQLiteDatabaseAdapter(BaseDatabaseAdapter):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self._engine = create_engine(
            self._settings.SQLITE_URL,
            echo=True,
            connect_args={"check_same_thread": False},
        )

    def connect(self) -> bool:
        SQLModel.metadata.create_all(self._engine)
        return True

    def create_pulse(
        self, tenant: str, product_sku: str, use_unity: str, used_amount: int
    ) -> bool:
        db_pulse = PulseModel(
            tenant=tenant,
            product_sku=product_sku,
            use_unity=use_unity,
            used_amount=used_amount,
        )
        with Session(self._engine) as session:
            session.add(db_pulse)
            session.commit()
        return True

    def get_pulses(self) -> Sequence[PulseData]:
        with Session(self._engine) as session:
            pulses = [
                PulseData(
                    tenant=pulse.tenant,
                    product_sku=pulse.product_sku,
                    use_unity=pulse.use_unity,
                    used_amount=pulse.used_amount,
                )
                for pulse in session.exec(select(PulseModel)).all()
            ]
        return pulses

    def disconnect(self) -> bool:
        return True
