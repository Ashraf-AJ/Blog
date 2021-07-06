import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from api.database.models import User as UserModel
from api.database import utils as db_utils


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = (
            "id",
            "password_hash",
            "role_id",
        )
        interfaces = (relay.Node,)

    followers_count = graphene.Field(graphene.Int)
    followers = relay.ConnectionField(lambda: FollowersConnection)
    following_count = graphene.Field(graphene.Int)
    following = relay.ConnectionField(lambda: FollowingConnection)

    def resolve_followers_count(instance, info):
        return instance.followers_count

    def resolve_following_count(instance, info):
        return instance.following_count

    def resolve_followers(instance, info):
        return instance.followers

    def resolve_following(instance, info):
        return instance.following


class FollowersConnection(graphene.Connection):
    class Meta:
        node = User


class FollowingConnection(graphene.Connection):
    class Meta:
        node = User


class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(User, description="The registered user")

    def mutate(instance, info, **input):
        user = db_utils.create(UserModel, **input)
        db_utils.save(user)

        return RegisterUser(user=user)


class Query(graphene.ObjectType):
    user = relay.Node.Field(User)
    users = SQLAlchemyConnectionField(User.connection)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
