from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Self
from uuid import UUID

import strawberry
import strawberry.fastapi
import strawberry.types

from open_transit import transit_type
from open_transit.networks import Network, NetworksRepository
from open_transit.routes import Route, RoutesRepository
from open_transit.stops import Stop, StopsRepository


@dataclass
class CustomContext(strawberry.fastapi.BaseContext):
    routes_repository: RoutesRepository
    networks_repository: NetworksRepository
    stops_repository: StopsRepository


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
class TransitStop:
    id: UUID
    name: str
    lat: Decimal
    lon: Decimal

    @classmethod
    def from_model(cls, model: Stop):
        return cls(
            id=model.id,
            name=model.name,
            lat=model.lat,
            lon=model.lon,
        )


@strawberry.type
class Query:
    @strawberry.field
    def networks(self, info: CustomInfo) -> list[TransitNetwork]:
        models = info.context.networks_repository.list()
        return list(map(TransitNetwork.from_model, models))

    @strawberry.field
    def network(self, info: CustomInfo, id: UUID) -> TransitNetwork | None:
        model = info.context.networks_repository.get(id)
        if model is None:
            return None
        return TransitNetwork.from_model(model)

    @strawberry.field
    def network_by_name(self, info: CustomInfo, name: str) -> TransitNetwork | None:
        model = info.context.networks_repository.get_by_name(name)
        if model is None:
            return None
        return TransitNetwork.from_model(model)

    @strawberry.field
    def routes(self, info: CustomInfo) -> list[TransitRoute]:
        models = info.context.routes_repository.list()
        return list(map(TransitRoute.from_model, models))

    @strawberry.field
    def route(self, info: CustomInfo, id: UUID) -> TransitRoute | None:
        model = info.context.routes_repository.get(id)
        if model is None:
            return None
        return TransitRoute.from_model(model)

    @strawberry.field
    def stops(self, info: CustomInfo) -> list[TransitStop]:
        models = info.context.stops_repository.list()
        return list(map(TransitStop.from_model, models))

    @strawberry.field
    def stops_in_rectangle(
        self,
        info: CustomInfo,
        min_lat: Decimal,
        min_lon: Decimal,
        max_lat: Decimal,
        max_lon: Decimal,
    ) -> list[TransitStop]:
        models = info.context.stops_repository.list_in_rectangle(
            min_lat=min_lat,
            min_lon=min_lon,
            max_lat=max_lat,
            max_lon=max_lon,
        )
        return list(map(TransitStop.from_model, models))


schema = strawberry.Schema(query=Query)
