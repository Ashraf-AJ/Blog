import pytest
from api.database.seeders import Roles, insert_roles_permissions
from api.database.models import User, Follow, Role, Permission


@pytest.fixture(scope="module")
def init_db(db):
    insert_roles_permissions(Role, Permission)


@pytest.fixture
def FollowModel(db, init_db):
    yield Follow
    Follow.query.delete()
    db.session.commit()


@pytest.fixture(scope="module")
def admin_role(db, init_db):
    admin_role = Role.query.filter_by(name=Roles.ADMINISTRATOR.value).first()
    return admin_role


@pytest.fixture(scope="module")
def user_role(db, init_db):
    user_role = Role.query.filter_by(name=Roles.USER.value).first()
    return user_role


@pytest.fixture
def users(db, init_db, user_role):
    user_a = User(name="a", username="a", password="a", email="a")
    user_b = User(name="b", username="b", password="b", email="b")
    db.session.add_all([user_a, user_b])
    db.session.commit()
    yield user_a, user_b
    db.session.delete(user_a)
    db.session.delete(user_b)
    db.session.commit()


@pytest.fixture
def admin_user(db, init_db, admin_role):
    admin_user = User(
        name="admin",
        username="admin",
        password="admin",
        email="admin",
        role_id=admin_role.id,
    )
    db.session.add(admin_user)
    db.session.commit()
    yield admin_user
    db.session.delete(admin_user)
    db.session.commit()


def test_user_default_role(users, user_role):
    u1, u2 = users

    assert u1.role_id == user_role.id
    assert u1.role == user_role
    assert u2.role_id == user_role.id
    assert u2.role == user_role


def test_user_is_admin(admin_user, users):
    u1, u2 = users

    assert u1.is_admin() is False
    assert u2.is_admin() is False
    assert admin_user.is_admin() is True


def test_user_follow(FollowModel, users):
    u1, u2 = users
    u1.follow(u2)
    data = FollowModel.query.first()

    assert data is not None
    assert u1.is_following(u2) is True
    assert u2.is_followed_by(u1) is True


def test_user_unfollow(FollowModel, users):
    u1, u2 = users
    u1.follow(u2)
    u1.unfollow(u2)
    data = FollowModel.query.first()

    assert data is None
    assert u1.is_following(u2) is False
    assert u2.is_followed_by(u1) is False


def test_user_update_timestamp(db, users):
    u1, u2 = users
    assert u1.updated_at is None
    assert u2.updated_at is None

    u1.name = "updated"
    db.session.add(u1)
    db.session.commit()

    assert u1.name == "updated"
    assert u1.updated_at is not None
    assert u2.updated_at is None


def test_followers_count(users):
    u1, u2 = users

    u1.follow(u2)

    assert u2.followers_count == 1
    assert u1.followers_count == 0


def test_following_count(users):
    u1, u2 = users

    u1.follow(u2)

    assert u1.following_count == 1
    assert u2.following_count == 0
