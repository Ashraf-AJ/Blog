from api import db
from api.database.models import User


def get_user(email, password):
    """
    checks if the credentials belong to a valid user and returns that user,
    otherwise raises a `GraphQLError`
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return
    if not user.check_password(password):
        return
    return user


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


# Managing database models' objects
def save(obj):
    db.session.add(obj)
    db.session.commit()


def create(model, **data):
    obj = model(**data)
    return obj
