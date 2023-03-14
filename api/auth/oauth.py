from functools import wraps
from flask_restx import abort
from http import HTTPStatus
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def admin_required(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                abort(HTTPStatus.FORBIDDEN, "You are not authorized to perform this action!")

        return decorator

