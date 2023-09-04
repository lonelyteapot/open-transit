from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from open_transit.graphql_api import schema
from open_transit.logging import configure_logging
from open_transit_private.graphql_context import get_graphql_context


def create_app() -> FastAPI:
    configure_logging()

    graphql_app = GraphQLRouter(
        schema,
        path="/",
        context_getter=get_graphql_context,
    )

    app = FastAPI()
    app.include_router(graphql_app)
    return app
