from flask import Flask, render_template, redirect, url_for, session
from config import Config
from routes.auth_routes import auth_bp
from routes.faculty_routes import faculty_bp
from routes.student_routes import student_bp
from routes.api_routes import api_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(student_bp)
app.register_blueprint(api_bp)

# ----------- Home -----------
@app.route("/")
def home():
    return render_template("index.html", user=session.get("user"))

# ----------- Dashboard Redirect -----------
@app.route("/dashboard")
def dashboard_redirect():
    if "user" in session:
        if session["user"]["role"] == "faculty":
            return redirect(url_for("faculty.dashboard"))
        return redirect(url_for("student.dashboard"))
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)