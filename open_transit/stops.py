from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List
from uuid import UUID


@dataclass
class Stop:
    id: UUID
    name: str
    lat: Decimal
    lon: Decimal
    importer_extra: Any = None


class StopsRepository(ABC):
    @abstractmethod
    def list(self) -> List[Stop]:
        ...

    @abstractmethod
    def list_in_rectangle(
        self,
        min_lat: Decimal,
        min_lon: Decimal,
        max_lat: Decimal,
        max_lon: Decimal,
    ) -> List[Stop]:
        ...

    @abstractmethod
    def get(self, id: UUID) -> Stop | None:
        ...
