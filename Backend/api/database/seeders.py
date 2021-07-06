from random import randint
from enum import Enum, auto
from sqlalchemy.exc import IntegrityError
from faker import Faker
from api import db
from api.database import models


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


def users(count=50):
    fake = Faker()
    i = 0
    while i < count:
        u = models.User(
            name=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            password="password",
            confirmed=True,
            location=fake.city(),
            about=fake.text(),
            created_at=fake.past_datetime(),
        )
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        else:
            print(f"user#{i} created!")
            i += 1


def posts(count=100):
    fake = Faker()
    users_count = models.User.query.count()
    for _ in range(count):
        p = models.Post(
            title="generic title",
            body=fake.text(),
            created_at=fake.past_datetime(),
            # randint is inclusive, [1, users_count]
            author=models.User.query.get(randint(1, users_count)),
        )
        db.session.add(p)
    db.session.commit()


def followings(count=100):
    i = 0
    users_count = models.User.query.count()
    while i < count:

        follower_id, followed_id = 0, 0
        while follower_id == followed_id:
            follower_id = randint(1, users_count)
            followed_id = randint(1, users_count)

        u1 = models.User.query.get(follower_id)
        u2 = models.User.query.get(followed_id)

        if not u1.is_following(u2):
            u1.follow(u2)
            i += 1
    db.session.commit()
