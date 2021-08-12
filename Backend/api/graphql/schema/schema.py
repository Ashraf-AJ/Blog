from graphene import relay, ObjectType, Schema
from . import user_type, auth_type, post_type, comment_type


class Query(comment_type.Query, post_type.Query, user_type.Query, ObjectType):
    node = relay.Node.Field()


class Mutation(
    comment_type.Mutation,
    post_type.Mutation,
    auth_type.Mutation,
    user_type.Mutation,
    ObjectType,
):
    pass


schema = Schema(query=Query, mutation=Mutation)
