from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class ConfigurationForm(FlaskForm):
    lidarr_sync = StringField("Lidarr Sync (True/False):", validators=[DataRequired()])
    plex_users = StringField(
        "Plex Users (comma-separated):", validators=[DataRequired()]
    )
    worker_count = IntegerField("Worker Threads:", validators=[DataRequired()])
    seconds_interval = IntegerField(
        "Schedule Interval (seconds):", validators=[DataRequired()]
    )
    manual_playlists = StringField(
        "Manual Playlists (True/False):", validators=[DataRequired()]
    )
    submit = SubmitField("Save Configuration")


class RunForm(FlaskForm):
    submit = SubmitField("Run Sync")
