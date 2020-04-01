"""All public configuration of application"""
import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(base_dir, '.env'))


class BaseConfig:
    DEBUG = False
    SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RECAPTCHA_PUBLIC_KEY = 'to be'
    RECAPTCHA_PRIVATE_KEY = 'to be '

class ProductionConfig(BaseConfig):
    pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'