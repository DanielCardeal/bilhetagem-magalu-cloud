from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Lock
from typing import Sequence

from app.settings import Settings
from app.data import PulseData


class AsyncSingleton(type):
    _instances = {}
    _instance_lock = Lock()

    def __call__(cls, *args, **kwargs) -> BaseDatabaseAdapter:
        with cls._instance_lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(BaseDatabaseAdapter, cls).__call__(
                    *args, **kwargs
                )
        return cls._instances[cls]


class BaseDatabaseAdapter(ABC):
    __metaclass__ = AsyncSingleton

    def __init__(self, settings: Settings):
        self._settings = settings

    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def create_pulse(
        self, tenant: str, product_sku: str, use_unity: str, used_amount: int
    ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_pulses(self) -> Sequence[PulseData]:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> bool:
        raise NotImplementedError()
