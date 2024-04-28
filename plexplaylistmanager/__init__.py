import os

from flask import Flask
from flask_bootstrap import Bootstrap5

from plexplaylistmanager.modules.plex.main import PlexService


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "ppm.db"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    Bootstrap5(app)
    with app.app_context():
        app.plex_service = PlexService()

    # Import routes
    from .routes import init_app_routes

    init_app_routes(app)

    return app
