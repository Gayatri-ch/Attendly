from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def login_required(role=None):
    """Decorator to enforce login and optional role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                flash("Please login to access this page.")
                return redirect(url_for("auth.login"))
            
            if role and session["user"]["role"] != role:
                # This will redirect to the main dashboard logic which handles role routing
                return redirect(url_for("dashboard_redirect"))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
