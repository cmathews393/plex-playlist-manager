from flask import Flask, render_template, request, blueprints
import os
from flask_executor import Executor
from .spotiplexinit import playlistsync
#import .spotify as sp
# import lidarr as lidarr
# import plex as plex
# import trakt as trakt
# import tmdb as tmdb
# import sonarr as sonarr

is_syncing = False

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    executor = Executor(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def home():
        return render_template("index.html.j2")

    @app.route("/config")
    def searchform():
        return render_template("config.html.j2")

    @app.route("/syncing")
    def syncing():
        global is_syncing
        if not is_syncing:
            is_syncing = True
            executor.submit(playlistsync)
        return render_template("syncing.html.j2")

    return app