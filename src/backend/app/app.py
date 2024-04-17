#!/usr/bin/python3
"""App main module"""

from flask import render_template, Flask
from .models import storage as db
from .models.cause import Cause
from .models.user import User

app = Flask(__name__)


@app.route("/")
def index():
    """Index page"""
    all_causes = db.all(User)
    print(all_causes)
    return render_template("index.html", users=all_causes)

@app.route("/login")
def login():
    """Login page"""
    return render_template('login.html')

@app.route("/create_user/")
def create_user():
    """Create user route"""
    return "<h1>Create User</h1>"


@app.route("/signup")
def signup():
    """Sign up page"""
    return "<h1>Sign Up</h1>"




@app.route("/dashboard")
# @login_required
def dashboard():
    """Dashboard page"""
    return "<h1>Dashboard</h1>"


@app.route("/donate")
def donate():
    """Donate page"""
    return "<h1>Donate</h1>"


@app.route("/logout")
def logout():
    """Logout"""
    return "<h1> Home Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)
