from importlib import import_module

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ._config import config
from .commons.error_handlers import register_error_handlers
from .commons.exceptions import Unauthorized

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

jwt = JWTManager(app)


@jwt.invalid_token_loader
def invalid_token_callback(message):
    return Unauthorized(error_message=f"Invalid token: {message}").to_response()


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


register_subpackages()
register_error_handlers(app)
