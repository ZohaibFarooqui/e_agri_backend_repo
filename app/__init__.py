from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.home_routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(home_bp, url_prefix="/")

    return app
