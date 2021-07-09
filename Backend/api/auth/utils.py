from flask_jwt_extended import create_access_token, create_refresh_token


def generate_access_token(
    identity,
    fresh=False,
    expires_delta=None,
    additional_claims=None,
    additional_headers=None,
):
    return create_access_token(
        identity,
        fresh,
        expires_delta,
        additional_claims,
        additional_headers,
    )


def generate_refresh_token(
    identity,
    expires_delta=None,
    additional_claims=None,
    additional_headers=None,
):
    return create_refresh_token(
        identity,
        expires_delta,
        additional_claims,
        additional_headers,
    )


def generate_confirmation_token(
    identity,
    fresh=False,
    expires_delta=None,
    additional_claims=None,
    additional_headers=None,
):
    return create_access_token(
        identity,
        fresh,
        expires_delta,
        additional_claims,
        additional_headers,
    )
