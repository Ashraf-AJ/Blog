import pytest
from api.database.models import Permission, Role, role_permission
from api.database.seeders import (
    Roles,
    Permissions,
    get_model_object,
    insert_roles_permissions,
)


@pytest.fixture
def cache():
    return {}


@pytest.fixture
def RoleModel(db):
    yield Role
    Role.query.delete()
    db.session.commit()


@pytest.fixture
def PermissionModel(db):
    yield Permission
    Permission.query.delete()
    db.session.commit()


def test_permissions_values():
    for permission in Permissions:
        assert permission.name == permission.value


def test_roles_values():
    for role in Roles:
        assert role.name == role.value


def test_get_model_object(RoleModel, cache):
    assert RoleModel.query.count() == 0

    role_object = get_model_object(
        Roles.USER, cache, RoleModel, name=Roles.USER.value
    )

    assert RoleModel.query.count() == 1
    assert RoleModel.query.filter_by(name=Roles.USER.value).first() is not None

    new_role_object = get_model_object(
        Roles.USER, cache, RoleModel, name=Roles.USER.value
    )

    assert new_role_object is role_object


def test_insert_roles_permissions(db, RoleModel, PermissionModel):
    assert db.session.query(role_permission).count() == 0
    assert RoleModel.query.count() == 0
    assert PermissionModel.query.count() == 0

    insert_roles_permissions(RoleModel, PermissionModel)

    assert db.session.query(role_permission).count() != 0
    assert RoleModel.query.count() == len(Roles)
    assert PermissionModel.query.count() == len(Permissions)
