from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, current_user
from api.errors import UnauthorizedError

# rewrite `jwt_required` decorator to add graphql error handling


def token_required(optional=False, fresh=False, refresh=False, locations=None):
    """
    ***rewrite of `jwt_required` decorator to add graphql error handling***

    A decorator to protect a Flask endpoint with JSON Web Tokens.

    Any route decorated with this will require a valid JWT to be present in the
    request (unless optional=True, in which case no JWT is also valid) before the
    endpoint can be called.

    :param optional:
        If ``True``, allow the decorated endpoint to be if no JWT is present in the
        request. Defaults to ``False``.

    :param fresh:
        If ``True``, require a JWT marked with ``fresh`` to be able to access this
        endpoint. Defaults to ``False``.

    :param refresh:
        If ``True``, requires a refresh JWT to access this endpoint. If ``False``,
        requires an access JWT to access this endpoint. Defaults to ``False``.

    :param locations:
        A location or list of locations to look for the JWT in this request, for
        example ``'headers'`` or ``['headers', 'cookies']``. Defaluts to ``None``
        which indicates that JWTs will be looked for in the locations defined by the
        ``JWT_TOKEN_LOCATION`` configuration option.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request(optional, fresh, refresh, locations)
            except Exception as e:
                raise UnauthorizedError(e.args[0])
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper


def has_permission(permission):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not current_user.role.can(permission):
                raise UnauthorizedError(
                    "You don't have a permission to perform this action"
                )
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper
