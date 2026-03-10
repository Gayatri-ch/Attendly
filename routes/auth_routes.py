from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
from utils.security import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        role = request.form["role"]
        uid = request.form["user_id"]
        password = hash_password(request.form["password"])

        if UserModel.create_user(uid, name, email, password, role):
            flash("Registration successful! Please login.")
            return redirect(url_for("auth.login"))
        flash("Error: UID or Email already exists.")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form["user_id"]
        password = request.form["password"]
        role = request.form["role"]

        user = UserModel.get_user_by_uid(uid, role)

        if user and verify_password(user["password"], password):
            session["user"] = {
                "id": user["id"],
                "uid": uid,
                "name": user["name"],
                "role": role
            }
            flash(f"Welcome back, {user['name']}!")
            return redirect(url_for("dashboard_redirect"))
        
        flash("Invalid credentials!")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for("auth.login"))
