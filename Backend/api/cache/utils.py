from flask import current_app
from flask_jwt_extended import get_jwt
from api import cache


def revoke_access_token():
    jti = get_jwt().get("jti")
    cache.jwt_blocklist.set(
        jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES")
    )


def check_if_blocked(key):
    return cache.jwt_blocklist.get(key) is not None
