"""App main module"""

import os
from pathlib import Path
from typing import cast
from flask import render_template, Flask, request
from hashlib import sha256 as hash_sha256

from app.models import database
from app.models.user import User
from app import algo

ROOT_DIR = Path(__file__).parent
UPLOAD_FOLDER = ROOT_DIR / "uploads"
if not UPLOAD_FOLDER.is_dir():
    os.mkdir(UPLOAD_FOLDER)
app = Flask(__name__)

@app.route("/")
def index():
    """Index page"""
    return render_template("index.html")


def save_uploaded_file(field_name: str) -> str:
    file = request.files[field_name]
    filename = cast(str, file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)
    return str(filepath)


@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        # Retrieve data from the request
        first_name = request.form.get("first_name")
        second_name = request.form.get("second_name")
        email = request.form.get("email")
        password = cast(str, request.form.get("password"))
        hashed_password = hash_sha256(password.encode()).hexdigest()
        profile_pic_url = save_uploaded_file("profile_photo")
        algo_account_address = algo.create_account()
        new_user = User(
            first_name=first_name,
            second_name=second_name,
            password=hashed_password,
            email=email,
            profile_pic_url=profile_pic_url,
            algo_account_address=algo_account_address,
        )
        # Add the new_user to the database session
        database.add(new_user)
    return "", 201



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


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
