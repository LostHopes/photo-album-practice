import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


class DevConfig(BaseConfig):
    pass