import os
from datetime import timedelta
from decouple import config

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
GRANDPARENT_DIR = os.path.abspath(os.path.join(PARENT_DIR, os.pardir))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    DEBUG = config('DEBUG', cast=bool)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES =  timedelta(minutes=60)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    ALGORITHM = config('ALGORITHM')
    ACCESS_TOKEN_EXPIRES_MINUTES = config('ACCESS_TOKEN_EXPIRES_MINUTES')



class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(GRANDPARENT_DIR, 'students.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True



class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    


class ProdConfig(Config):
    ...    



config_dict = {
    'dev': DevConfig,
    'testing' : TestConfig,
    'production' : ProdConfig,
}