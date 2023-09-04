from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class Network:
    id: UUID
    name: str
    importer_extra: Any = None


class NetworksRepository(ABC):
    @abstractmethod
    def list(self) -> list[Network]:
        ...
