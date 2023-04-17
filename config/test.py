import os

from .local import Config as _Config


class Config(_Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST",
        "mysql+pymysql://root:my-secret-pw@127.0.0.1/catalog_test",
    )
