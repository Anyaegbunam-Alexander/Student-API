from functools import wraps
from flask import request
from jose import jwt
from datetime import datetime, timedelta
from flask_restx import abort

from api.config.config import config_dict


app_env = 'dev'
config_class = config_dict[app_env]


SECRET_KEY = config_class.SECRET_KEY
ALGORITHM = config_class.ALGORITHM
ACCESS_TOKEN_EXPIRES_MINUTES = int(config_class.ACCESS_TOKEN_EXPIRES_MINUTES)


def create_access_token_admin(admin):
    to_encode = {'id' : admin.id}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp' : expire})
    to_encode.update({'is_administrator' : True})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    admin.access = encoded_jwt
    admin.token_type = 'bearer'


def create_access_token_non_admin(object):
    to_encode = {'id' : object.id}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp' : expire})
    to_encode.update({'is_administrator' : False})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    object.access = encoded_jwt
    object.token_type = 'bearer'
    


def token_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[len('Bearer '):]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                is_administrator = payload.get('is_administrator')
                id = payload.get('id')
                payload_dict = {'id' : id, 'is_administrator' : is_administrator}
            except:
                abort(401, 'Invalid or expired token')
            else:
                return fn(payload_dict=payload_dict, *args, **kwargs)
        else:
            abort(401, 'invalid or missing Authorization header')
    return decorator
