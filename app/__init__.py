from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .validation import register_error_handlers



db=SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trip_planner.db"
    db.init_app(app)

    from . import models
    from .routes import bp

    app.register_blueprint(bp)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app