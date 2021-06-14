import graphene
from graphene import relay
from graphene.relay import mutation
from . import user_type


class Query(user_type.Query, graphene.ObjectType):
    node = relay.Node.Field(id=graphene.ID())


class Mutation(user_type.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
