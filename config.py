from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)


class ConfigFactory:
    def factory():
        env = getenv("FLASK_ENV", "development")

        if env == "development":
            return Development()
        elif env == "testing":
            return Testing()
    
    factory = staticmethod(factory)


class Config:
    __abstract__ = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI')


class Testing(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_TESTING_URI')