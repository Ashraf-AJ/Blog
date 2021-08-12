from api import db
from api.database.models import User
from api.database.seeders import Permissions


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


def get_object_by_id(model, obj_id):
    return model.query.get(obj_id)


def can_modify_resource(resource, user):
    return user.role.can(Permissions.MODERATE.value) or resource.is_author(
        user
    )


# Managing database models' objects
def save(obj):
    db.session.add(obj)
    db.session.commit()


def create(model, **data):
    obj = model(**data)
    return obj


def update(obj, **kwargs):
    for attr, val in kwargs.items():
        setattr(obj, attr, val)
    save(obj)


def delete(obj):
    db.session.delete(obj)
    db.session.commit()
