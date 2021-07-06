from graphene import relay, ObjectType, Schema, ID
from . import user_type, auth_type


class Query(user_type.Query, ObjectType):
    node = relay.Node.Field(id=ID())


class Mutation(auth_type.Mutation, user_type.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)