import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from api.auth import current_user
from api.database.models import Post as PostModel
from api.database.seeders import Permissions
from api.database import utils as db_utils
from api.auth.decorators import token_required, has_permission
from api.errors import UnauthorizedError
from api.graphql import utils as gql_utils


class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        exclude_fields = ("id", "user_id")
        interfaces = (relay.Node,)

    author = graphene.Field(lambda: User)
    comments = relay.ConnectionField(lambda: CommentsConnection)

    def resolve_author(instance, info):
        return instance.author

    def resolve_comments(instance, info, **kwargs):
        return instance.comments


class CommentsConnection(relay.Connection):
    class Meta:
        from .comment_type import Comment

        node = Comment


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    post = graphene.Field(Post)

    @token_required()
    @has_permission(Permissions.WRITE.value)
    def mutate(instance, info, title, body):
        post = db_utils.create(
            PostModel,
            author=current_user._get_current_object(),
            title=title,
            body=body,
        )
        db_utils.save(post)
        return CreatePost(post=post)


class EditPost(graphene.Mutation):
    class Arguments:
        global_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    post = graphene.Field(Post)

    @token_required()
    def mutate(instance, info, global_id, title, body):
        edited_post = gql_utils.get_object_by_global_id(global_id)

        if not db_utils.can_modify_resource(edited_post, current_user):
            raise UnauthorizedError("You're not the author of this post")

        db_utils.update(
            edited_post,
            title=title,
            body=body,
        )
        return EditPost(post=edited_post)


class DeletePost(graphene.Mutation):
    class Arguments:
        global_id = graphene.ID(required=True)

    success = graphene.Boolean(default_value=False)

    @token_required()
    def mutate(instance, info, global_id):
        post_to_delete = gql_utils.get_object_by_global_id(global_id)

        if not db_utils.can_modify_resource(post_to_delete, current_user):
            raise UnauthorizedError("You're not the author of this post")

        db_utils.delete(post_to_delete)

        return DeletePost(success=True)


class Query(graphene.ObjectType):
    post = relay.Node.Field(Post)
    posts = SQLAlchemyConnectionField(Post.connection)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field(description="Create a new post")
    edit_post = EditPost.Field(description="Edit an existing post")
    delete_post = DeletePost.Field(description="Delete an existing post")


from .user_type import User
