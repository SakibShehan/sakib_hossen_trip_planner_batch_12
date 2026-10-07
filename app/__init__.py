from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trip_planner.db"

    db.init_app(app)

    from . import models
    from .routes import register_routes
    from .validators.errors import register_error_handlers

    register_routes(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app