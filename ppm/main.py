from flask import Flask, request, redirect, url_for, flash, render_template
from flask_bootstrap import Bootstrap5
from ppm.modules.confighandler.main import read_config, write_config


def check_and_update_first_run():
    """Check if it's the first run and update the configuration after setup."""
    config = read_config("ppm")
    if config.get("first_run", "True") == "True":  # Check if the first run flag is True
        return True
    return False


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ppmkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ppm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    bootstrap = Bootstrap5(app)

    from .routes import main_bp as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
