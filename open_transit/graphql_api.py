from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Self
from uuid import UUID

import strawberry
import strawberry.fastapi
import strawberry.types

from open_transit import transit_type
from open_transit.networks import Network, NetworksRepository
from open_transit.routes import Route, RoutesRepository


@dataclass
class CustomContext(strawberry.fastapi.BaseContext):
    routes_repository: RoutesRepository
    networks_repository: NetworksRepository


CustomInfo = strawberry.types.Info[CustomContext, None]


@strawberry.enum
class TransitType(StrEnum):
    bus = "bus"
    trolleybus = "trolleybus"
    tram = "tram"
    metro = "metro"

    @classmethod
    def from_model(cls, model: transit_type.TransitType) -> Self:
        match model:
            case transit_type.TransitType.bus:
                return cls.bus
            case transit_type.TransitType.trolleybus:
                return cls.trolleybus
            case transit_type.TransitType.tram:
                return cls.tram
            case transit_type.TransitType.metro:
                return cls.metro


@strawberry.type
class TransitNetwork:
    id: UUID
    name: str

    _model: strawberry.Private[Network]

    @classmethod
    def from_model(cls, model: Network):
        return cls(
            id=model.id,
            name=model.name,
            _model=model,
        )

    @strawberry.field
    def routes(self, info: CustomInfo) -> list[TransitRoute]:
        models = info.context.routes_repository.list_for_network(self._model)
        return list(map(TransitRoute.from_model, models))


@strawberry.type
class TransitRoute:
    id: UUID
    number: str
    title: str
    type: TransitType
    _model: strawberry.Private[Route]

    @classmethod
    def from_model(cls, model: Route):
        return cls(
            id=model.id,
            number=model.number,
            title=model.title,
            type=TransitType.from_model(model.type),
            _model=model,
        )


@strawberry.type
class Query:
    @strawberry.field
    def networks(self, info: CustomInfo) -> list[TransitNetwork]:
        models = info.context.networks_repository.list()
        return list(map(TransitNetwork.from_model, models))

    @strawberry.field
    def routes(self, info: CustomInfo) -> list[TransitRoute]:
        models = info.context.routes_repository.list()
        return list(map(TransitRoute.from_model, models))


schema = strawberry.Schema(query=Query)
