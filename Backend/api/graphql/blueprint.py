from flask import Blueprint
from .custom_graphql import CustomGraphqlView
from .schema import schema


graphql = Blueprint("graphql", __name__)


graphql.add_url_rule(
    "/graphql",
    view_func=CustomGraphqlView.as_view(
        "graphql", schema=schema, graphiql=True
    ),
)
