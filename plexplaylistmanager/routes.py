from flask import render_template, request, jsonify, flash, url_for, redirect, current_app
from flask_executor import Executor
from .ppm_modules.confighandler import read_config, write_config
from .ppm_modules import ppm
executor = Executor()

def init_app_routes(app):
    executor.init_app(app)
    config = read_config("ppm")
    @app.route("/")
    def home():
        return render_template("index.html.j2")

    @app.route("/preferences")
    def preferences():
        plex_users=current_app.plex_service.get_plex_users()
        config_data = read_config("ppm")
        checked_users = config_data.get("users", [])
        return render_template("preferences.html.j2", plex_users=plex_users, checked_users=checked_users)
    
    @app.route("/submit-preferences", methods=["POST"])
    def save_prefs():

        checked_users = [
            user for user in request.form
            if user.startswith('plex_user_') and request.form.get(user) == 'on'
        ]
        users = [user.split('_', 2)[2] for user in checked_users]  # Extract usernames from form data keys

        # Collecting notification preference
        notification_preference = request.form.get('notifications', 'none')

        # Collecting dark mode preference
        dark_mode_enabled = request.form.get('dark_mode', 'off') == 'on'

        # Prepare data to pass to the configuration function
        config_data = {
            "users": users,
            "notification_preference": notification_preference,
            "dark_mode_enabled": dark_mode_enabled
        }

        write_config("ppm", config_data)
        flash('Settings were saved successfully!', 'success')
        return redirect(url_for('config'))

    @app.route('/sync')
    def sync_dashboard():
        plex_users = config.get("users")
        # plex_users = current_app.plex_service.get_plex_users() 
        movies = ppm.radarr_tag_sync2(plex_users)  
        return render_template('syncing.html.j2', plex_users=plex_users, user_movies=movies)
    

    @app.route("/logs")
    def logs():
        return render_template("logs.txt")  # Make sure to handle text file rendering

    @app.route("/settings/<service>", methods=["GET"])
    def service_settings(service):
        config = read_config(service)
        return render_template("settings.html.j2", service=service, config=config, serviceproper=service.capitalize())

    @app.route("/<service>_submit", methods=["POST"])
    def submit_service_settings(service):
        api_key = request.form["api_key"]
        url = request.form["url"]
        write_config(service, {"api_key": api_key, "url": url})
        return jsonify({"message": f"{service.capitalize()} settings updated successfully!"})

