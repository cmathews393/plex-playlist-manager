import time

from flask import (
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_executor import Executor

from plexplaylistmanager import ppm
from plexplaylistmanager.modules.confighandler.main import read_config, write_config

executor = Executor()


def init_app_routes(app):
    executor.init_app(app)
    config = read_config("ppm")

    @app.route("/")
    def home():
        return render_template("index.html.j2")

    @app.route("/preferences")
    def preferences():
        plex_users = current_app.plex_service.get_plex_users()
        config_data = read_config("ppm")
        checked_users = config_data.get("users", [])
        return render_template(
            "preferences.html.j2",
            plex_users=plex_users,
            checked_users=checked_users,
        )

    @app.route("/submit-preferences", methods=["POST"])
    def save_prefs():
        checked_users = [
            user
            for user in request.form
            if user.startswith("plex_user_") and request.form.get(user) == "on"
        ]
        users = [
            user.split("_", 2)[2] for user in checked_users
        ]  # Extract usernames from form data keys

        config_data = {
            "users": users,
            # "notification_preference": notification_preference,
            # "dark_mode_enabled": dark_mode_enabled
        }

        write_config("ppm", config_data)
        flash("Settings were saved successfully!", "success")
        return redirect(url_for("preferences"))

    @app.route("/syncsettings")
    def syncsettings():
        return render_template("syncsettings.html.j2")

    @app.route("/sync")
    def sync_dashboard():
        start_time = time.time()  # Start timing

        plex = current_app.plex_service
        active_users = config.get(
            "users",
            [],
        )  # Fetch user list; assume default as empty list if not set

        # Get movies and shows keyed by user
        radarr_users, user_movies = ppm.radarr_tag_sync2(
            active_users,
        )  # Get only the second item from the tuple (dictionary)
        sonarr_users, user_shows = ppm.sonarr_tag_sync(
            active_users,
        )  # Get only the second item from the tuple (dictionary)
        lidarr_users, user_artists = ppm.lidarr_tag_sync(active_users)

        # Combine movies and shows into a single dictionary for each user
        user_items = {}
        all_users = set(user_movies.keys()).union(
            set(user_shows.keys()),
            set(user_artists.keys()),
        )  # Combine all unique users from both dicts
        for user in all_users:
            user_items[user] = {
                "movies": user_movies.get(user, []),
                "shows": user_shows.get(user, []),
                "artists": user_artists.get(user, []),
            }
        sorted_user_items = sorted(
            user_items.items(),
            key=lambda item: len(item[1]["movies"])
            + len(item[1]["shows"])
            + len(item[1].get("artists", ["Test"])),
            reverse=True,
        )

        elapsed_time = time.time() - start_time  # End timing
        print(f"Time elapsed: {elapsed_time:.2f} seconds")  # Print time elapsed

        return render_template(
            "syncing.html.j2",
            plex_users=active_users,
            user_items=sorted_user_items,
        )

    @app.route("/start-sync", methods=["POST"])
    def start_sync():
        # Flash message to user
        flash("Sync has started!", "success")

        # Redirect back to the sync dashboard
        return redirect(url_for("sync_dashboard"))

    @app.route("/logs")
    def logs():
        return render_template("logs.txt")  # Make sure to handle text file rendering

    @app.route("/settings/<service>", methods=["GET"])
    def service_settings(service):
        config = read_config(service)
        return render_template(
            "settings.html.j2",
            service=service,
            config=config,
            serviceproper=service.capitalize(),
        )

    @app.route("/<service>_submit", methods=["POST"])
    def submit_service_settings(service):
        api_key = request.form["api_key"]
        url = request.form["url"]
        write_config(service, {"api_key": api_key, "url": url})
        return jsonify(
            {"message": f"{service.capitalize()} settings updated successfully!"},
        )
