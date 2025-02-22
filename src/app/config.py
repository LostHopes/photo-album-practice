import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///:memory:"
    )
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True
    B2_KEY_ID = os.getenv("B2_KEY_ID")
    B2_KEY = os.getenv("B2_KEY")
    BUCKET_ID = os.getenv("BUCKET_ID")


class ProdConfig(BaseConfig):
    DEBUG = False


class DevConfig(BaseConfig):
    pass
