from graphene_sqlalchemy import SQLAlchemyObjectType
from api.database.models import Comment as CommentModel


class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        exclude_fields = ("id", "post_id", "user_id")
