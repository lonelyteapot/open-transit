from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List
from uuid import UUID

from open_transit.networks import Network
from open_transit.transit_type import TransitType


@dataclass
class Route:
    id: UUID
    number: str
    title: str
    type: TransitType
    importer_extra: Any = None


class RoutesRepository(ABC):
    @abstractmethod
    def list(self) -> List[Route]:
        ...

    @abstractmethod
    def list_for_network(self, network: Network) -> List[Route]:
        ...
