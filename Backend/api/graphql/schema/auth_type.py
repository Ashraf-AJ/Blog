import graphene
from api.auth.decorators import token_required
from api.auth import current_user, utils as auth_utils
from api.database import utils as db_utils
from api.cache import utils as cache_utils
from api.errors import UnauthorizedError


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String(
        description="The token used for authentication"
    )
    refresh_token = graphene.String(
        description="The token used to request a new access token"
    )

    def mutate(instance, info, email, password):
        user = db_utils.get_user(email, password)
        if not user:
            raise UnauthorizedError("Invalid Credentials")
        access_token = auth_utils.generate_access_token(identity=user.id)
        refresh_token = auth_utils.generate_refresh_token(identity=user.id)
        return Login(access_token=access_token, refresh_token=refresh_token)


class Logout(graphene.Mutation):
    msg = graphene.String()

    @token_required()
    def mutate(instance, info):
        cache_utils.revoke_access_token()
        return Logout(msg="AccessToken revoked")


class Refresh(graphene.Mutation):
    access_token = graphene.String(
        description="The token used for authentication"
    )

    @token_required(refresh=True)
    def mutate(instance, info):
        access_token = auth_utils.generate_access_token(
            identity=current_user.id
        )
        return Refresh(access_token=access_token)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    logout = Logout.Field()
    refresh = Refresh.Field()
