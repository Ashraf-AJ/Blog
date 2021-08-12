from api import jwt
from api.database import models, utils as db_utils
from api.cache import utils as cache_utils


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data.get("sub")
    return db_utils.get_object_by_id(models.User, identity)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    return cache_utils.check_if_blocked(jti)
