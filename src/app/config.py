import os
import logging
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(
#     filename="app.log",
#     level=logging.ERROR,
#     format="%(asctime)s %(levelname)s %(name)s : %(message)s",
# )


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


class TestConfig(BaseConfig):
    SECRET_KEY = "yoursecretkey"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
