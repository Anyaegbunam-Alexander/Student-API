import os
from datetime import timedelta
from decouple import config

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
GRANDPARENT_DIR = os.path.abspath(os.path.join(PARENT_DIR, os.pardir))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES =  timedelta(minutes=60)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    ALGORITHM = config('ALGORITHM')
    ACCESS_TOKEN_EXPIRES_MINUTES = config('ACCESS_TOKEN_EXPIRES_MINUTES')



class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(GRANDPARENT_DIR, 'students.db')


class TestConfig(Config):
    ...


class ProdConfig(Config):
    ...    



config_dict = {
    'dev': DevConfig,
    'test' : TestConfig,
    'prod' : ProdConfig,
}