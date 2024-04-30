from flask import Flask
from flask_bootstrap import Bootstrap5


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ppmkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ppm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    bootstrap = Bootstrap5(app)

    from .routes import main_bp as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
