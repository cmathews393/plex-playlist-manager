from flask import Blueprint, Flask, flash, redirect, render_template, url_for

from ppm.forms import ConfigurationForm, RunForm  # Corrected from RunForms to RunForm

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "your_secret_key"  # Ensure you set a secret key for session management
)


main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def home():
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
