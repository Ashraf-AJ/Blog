import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from api.database.models import Post as PostModel


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


class Query(graphene.ObjectType):
    post = relay.Node.Field(Post)
    posts = SQLAlchemyConnectionField(Post.connection)


from .comment_type import Comment
from .user_type import User
