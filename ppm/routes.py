from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for

from ppm.forms import ConfigurationForm, RunForm  # Corrected from RunForms to RunForm
from ppm.main import check_and_update_first_run
from ppm.modules.confighandler.main import write_config

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "your_secret_key"  # Ensure you set a secret key for session management
)


main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        # Assume setup form has been filled out and now you're processing it
        # Process your form data here and save it
        write_config(
            "ppm", {"first_run": "False"}
        )  # Set the first run flag to False after setup
        flash("Setup complete! Configuration saved.")
        return redirect(url_for("home"))

    # Only show setup if it's the first run
    if check_and_update_first_run():
        return render_template("setup.html.j2")
    else:
        return redirect(url_for("home"))


@main_bp.route("/")
def home():
    if check_and_update_first_run():
        return render_template("setup.html.j2")
    return render_template("home.html.j2")


@main_bp.route("/about")
def about():
    return render_template("about.html.j2")


@main_bp.route("/music", methods=["GET", "POST"])
def music():
    form = ConfigurationForm()
    run_form = RunForm()
    if form.validate_on_submit():
        # Process the data from form
        flash("Configuration Saved!")
        return redirect(
            url_for("main.music")
        )  # Changed to 'main.music' to indicate Blueprint
    return render_template("music.html.j2", form=form, run_form=run_form)


@main_bp.route("/run", methods=["POST"])
def run_spotiplex():
    # Trigger Spotiplex run function
    flash("Spotiplex is running!")
    return redirect(
        url_for("main.home")
    )  # Changed to 'main.home' to indicate Blueprint


app.register_blueprint(main_bp)  # Register the Blueprint with the Flask application

if __name__ == "__main__":
    app.run(debug=True)
