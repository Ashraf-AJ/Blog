import graphene
from flask import current_app
from api.auth.decorators import token_required
from api.auth import current_user, utils as auth_utils
from api.database import utils as db_utils
from api.cache import utils as cache_utils
from api.errors import ForbiddenError, UnauthorizedError
from api.email import send_email


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


class SendConfirmationEmail(graphene.Mutation):
    sent = graphene.Boolean()

    @token_required()
    def mutate(instance, info):
        if current_user.confirmed:
            raise ForbiddenError("Your account is alreday confirmed!")

        send_email(
            "testing email service",
            "ashraf.aj7@gmail.com",  # replace with current_user.email
            template="emails/confirm_account",
            user=current_user,
            token=auth_utils.generate_confirmation_token(
                identity=current_user.id,
                expires_delta=current_app.config.get(
                    "APP_JWT_CONFIRMATION_TOKEN_EXPIRES"
                ),
            ),
        )
        return SendConfirmationEmail(sent=True)


class ConfirmUserAccount(graphene.Mutation):
    confirmed = graphene.Boolean()

    @token_required()
    def mutate(instance, info):
        if current_user.confirmed:
            raise ForbiddenError("Your account is alreday confirmed!")

        db_utils.update(current_user, confirmed=True)
        return ConfirmUserAccount(confirmed=True)


class Mutation(graphene.ObjectType):
    login = Login.Field()
    logout = Logout.Field()
    refresh = Refresh.Field()
    send_confirmation_email = SendConfirmationEmail.Field()
    confirm_user_account = ConfirmUserAccount.Field()
