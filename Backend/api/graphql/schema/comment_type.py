import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from api.database.models import (
    Comment as CommentModel,
    Post as PostModel,
)
from api.database.seeders import Permissions
from api.database import utils as db_utils
from api.graphql import utils as gql_utils
from api.auth.decorators import has_permission, token_required
from api.auth import current_user
from api.errors import UnauthorizedError


class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        exclude_fields = ("id", "post_id", "user_id")

    author = graphene.Field(lambda: User)

    def resolve_author(instance, info):
        return instance.author


class CreateComment(graphene.Mutation):
    class Arguments:
        post_global_id = graphene.ID(required=True)
        body = graphene.String(required=True)

    comment = graphene.Field(Comment)

    @token_required()
    @has_permission(Permissions.COMMENT.value)
    def mutate(instance, info, post_global_id, body):
        post = gql_utils.get_object_by_global_id(PostModel, post_global_id)

        comment = db_utils.create(
            CommentModel,
            author=current_user._get_current_object(),
            post=post,
            body=body,
        )
        db_utils.save(comment)

        return CreateComment(comment=comment)


class EditComment(graphene.Mutation):
    class Arguments:
        global_id = graphene.ID(required=True)
        body = graphene.String(required=True)

    comment = graphene.Field(Comment)

    @token_required()
    def mutate(instance, info, global_id, body):
        edited_comment = gql_utils.get_object_by_global_id(global_id)

        if not db_utils.can_modify_resource(edited_comment, current_user):
            raise UnauthorizedError("You're not the author of this comment")

        db_utils.update(
            edited_comment,
            body=body,
        )
        return EditComment(comment=edited_comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        global_id = graphene.ID(required=True)

    success = graphene.Boolean(default_value=False)

    @token_required()
    def mutate(instance, info, global_id):
        comment_to_delete = gql_utils.get_object_by_global_id(global_id)

        if not db_utils.can_modify_resource(comment_to_delete, current_user):
            raise UnauthorizedError("You're not the author of this comment")

        db_utils.delete(comment_to_delete)

        return DeleteComment(success=True)


class Query(graphene.ObjectType):
    comment = relay.Node.Field(Comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field(
        description="Create a new comment on a comment"
    )
    edit_comment = EditComment.Field(description="Edit an existing comment")
    delete_comment = DeleteComment.Field(
        description="Delete an existing comment"
    )


from .user_type import User
