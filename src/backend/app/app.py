#!/usr/bin/python3
"""App main module"""

import os
from pathlib import Path
from typing import Any, TypeVar, cast
from flask import Response, jsonify, render_template, Flask, request
from werkzeug.security import check_password_hash, generate_password_hash

from .models import database
from .models.user import User
from .models.cause import Cause
from .models.donation import Donation

# from app import algo

ROOT_DIR = Path(__file__).parent
UPLOAD_FOLDER = ROOT_DIR / "uploads"
if not UPLOAD_FOLDER.is_dir():
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)

T = TypeVar("T")


def _id(obj_id: str) -> str:
    """ Returns object id from full instance id
        NB: instance id is returned as <CLASS>.<instance_id> from db.all()
    """
    return obj_id.split(".")[1]

@app.route("/")
def index():
    """Index page"""
    all_causes = database.all(Cause)
    causes = list()
    for u in all_causes:
        obj_id = _id(u)
        obj = database.get(Cause, obj_id)
        causes.append(obj)
    return render_template("index.html", causes=causes)


def save_uploaded_file(field_name: str) -> str:
    file = unwrap(request.files.get(field_name))
    filename = unwrap(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)
    return str(filepath)


def unwrap(optional: T | None) -> T:
    return cast(T, optional)


def error_response(message: str) -> Response:
    return jsonify({"status": "error", "message": message})


def success_response(data: dict[str, Any] | None = None) -> Response:
    return jsonify({"status": "success", "data": data})


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    users = (
        database.session.query(User)
        .filter_by(
            email=email,
        )
        .all()
    )

    # NOTE: It is insecure to give specific error messages i.e., telling the user
    # that the password specifically is what is invalids reveals that the email
    # exists in our database, but for better easier debugging during devt I've kept it
    if not users:
        return error_response("Invalid email"), 401
    users_dicts = [u.to_dict() for u in users]
    password = unwrap(request.form.get("password"))
    target_users = [
        u for u in users_dicts if check_password_hash(u["hashed_password"], password)
    ]
    if not target_users:
        return error_response("Invalid password"), 401
    user = target_users[0]
    return user, 200


@app.route("/signup", methods=["POST"])
def signup():
    first_name = request.form.get("first_name")
    second_name = request.form.get("second_name")
    email = request.form.get("email")
    potential_user = database.session.query(User).filter_by(email=email).first()
    if potential_user is not None:
        return error_response("Account already exists"), 409
    password = cast(str, request.form.get("password"))
    hashed_password = generate_password_hash(password)
    profile_pic_url = save_uploaded_file("profile_photo")
    algo_account_address = algo.create_account()
    new_user = User(
        first_name=first_name,
        second_name=second_name,
        hashed_password=hashed_password,
        email=email,
        profile_pic_url=profile_pic_url,
        algo_account_address=algo_account_address,
    )
    # Add the new_user to the database session
    database.add(new_user)
    return success_response(), 201


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
