import datetime
import logging
import os


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:my-secret-pw@127.0.0.1/catalog"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my-secret-jwt")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
