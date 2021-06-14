from enum import Enum, auto
from api import db


class AutoName(Enum):
    """override automatic-value generation"""

    def _generate_next_value_(name, start, count, last_values):
        """
        the enum's value becomes its own name:
            class C(AutoName):
                ENUM1 = auto()
                ENUM2 = auto()

            list(C) -> [<C.ENUM1: 'ENUM1'>, <C.ENUM2: 'ENUM2'>
        """
        return name


class Permissions(AutoName):
    FOLLOW = auto()
    WRITE = auto()
    COMMENT = auto()
    MODERATE = auto()
    ADMIN = auto()


class Roles(AutoName):
    USER = auto()
    MODERATOR = auto()
    ADMINISTRATOR = auto()


roles_permissions = {
    Roles.USER: [Permissions.FOLLOW, Permissions.WRITE, Permissions.COMMENT],
    Roles.MODERATOR: [
        Permissions.FOLLOW,
        Permissions.WRITE,
        Permissions.COMMENT,
        Permissions.MODERATE,
    ],
    Roles.ADMINISTRATOR: [
        Permissions.FOLLOW,
        Permissions.WRITE,
        Permissions.COMMENT,
        Permissions.MODERATE,
        Permissions.ADMIN,
    ],
}


def create_model_object(model, **data):
    obj = model(**data)
    db.session.add(obj)
    db.session.commit()
    return obj


def get_model_object(key, cache, model, **data):
    model_object = cache.get(key, None)
    if model_object is None:
        model_object = create_model_object(model, **data)
        cache[key] = model_object
    return model_object


def insert_roles_permissions(role_model, permission_model):
    cache = {}
    for role, permissions in roles_permissions.items():
        role_object = get_model_object(
            role, cache, role_model, name=role.value
        )
        for permission in permissions:
            permission_object = get_model_object(
                permission, cache, permission_model, name=permission.value
            )
            role_object.permissions.append(permission_object)
    db.session.commit()


# Managing database models' objects
def save(obj):
    db.session.add(obj)
    db.session.commit()
