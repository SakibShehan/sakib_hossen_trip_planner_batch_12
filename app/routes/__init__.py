from .health import health_bp
from .trips import trips_bp
from .travelers import travelers_bp
from .expenses import expenses_bp
from .summary import summary_bp

def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(travelers_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(summary_bp)