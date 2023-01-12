import os

from flask import Flask

from app.constants import (
    default_timeout,
    default_timeout_env,
    default_timeout_value,
)
from app.web import info, load


def create_app() -> Flask:
    app = Flask("Main application")
    app.config[default_timeout] = os.environ.get(
        default_timeout_env, default_timeout_value
    )

    app.register_blueprint(info.bp)
    app.register_blueprint(load.bp)

    return app


application = create_app()
