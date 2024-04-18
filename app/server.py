#!/usr/bin/python3
"""App main module (controller and service)"""

import os
from pathlib import Path
from typing import Any, TypeVar, cast
from flask import Response, jsonify, Flask, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from flask.templating import render_template
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib

from app.models import database
from app.models.user import User
from app.models.cause import Cause
import time
# from app import algo

ROOT_DIR = Path(__file__).parent
UPLOAD_FOLDER = ROOT_DIR / "uploads"
if not UPLOAD_FOLDER.is_dir():
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # TODO : replace with more secure?

T = TypeVar("T")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """ User loader for session mngt """
    return database.session.query(User).get(user_id)


def hash_password(password):
    """Basic: Hashes a password using SHA-256."""
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()


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


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard", user_id=current_user.id))
    causes = database.all(Cause)
    all_causes = list()
    for cause in causes.values():
        all_causes.append(cause.to_dict())
    print(all_causes)
    return render_template("index.html", causes=causes)


@app.route("/signup/", methods=["POST", "GET"], strict_slashes=False)
def signup():
    if request.method == "GET":
        return render_template("login.html")

    print("Signing up")
    print(request.form)
    first_name = request.form.get("f-name")
    second_name = request.form.get("l-name")
    email = request.form.get("email")
    potential_user = database.session.query(User).filter_by(email=email).first()
    if potential_user is not None:
        time.sleep(5)  # for user to see the message?
        return redirect(url_for("login"))

    password = cast(str, request.form.get("password"))
    hashed_password = generate_password_hash(password)
    # hashed_password = hash_password(password)
    # profile_pic_url = save_uploaded_file("profile_photo")
    profile_pic_url = None
    user = User(
        first_name=first_name,
        second_name=second_name,
        hashed_password=hashed_password,
        email=email,
        profile_pic_url=profile_pic_url,
    )
    # Add the new_user to the database session
    database.add(user)
    if not user:
        return redirect(url_for("signup"))
    print("User created")
    print(user.to_dict())
    return redirect(url_for("login"))


@app.route("/login/", methods=["POST", "GET"], strict_slashes=False)
def login():
    if request.method == "GET":
        return render_template("login.html")

    print("Logging in")
    print(request.form)
    email = request.form.get("email")
    password = unwrap(request.form.get("password"))

    # assuming user cannot have multiple accounts with same password
    user = (
        database.session.query(User)
        .filter_by(
            email=email,
        )
        .all()
    )[0]

    # NOTE: It is insecure to give specific error messages i.e., telling the user
    # that the password specifically is what is invalids reveals that the email
    # exists in our database, but for better easier debugging during devt I've kept it
    if not user:
        return error_response("Invalid email"), 401

    print(user.to_dict())
    if check_password_hash(user.hashed_password, password):
        login_user(user)
        print(current_user.is_authenticated)
        return redirect(url_for("dashboard", user_id=user.id))

    return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"], strict_slashes=False)
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Dashboard"""
    user_id = request.args.get("user_id")
    # Now you have access to the user_id
    print(user_id)
    print(current_user)
    # get user
    # get user's causes
    # get user's donations
    return render_template("dashboard.html")


@app.route("/causes", methods=["GET"])
def causes():
    all_causes = database.session.query(Cause).all()
    all_causes_dict = [c.to_dict() for c in all_causes]
    data = {"causes": all_causes_dict}
    return success_response(data), 200


@app.route("/create-cause", methods=["POST, GET"], strict_slashes=False)
@login_required
def create_cause():
    """ create a cause """
    if request.method == "GET":
        return render_template("createcause.html")
    
    print(request.form)
    user_id = request.args.get("user_id")
    name = request.form.get("name")
    description = request.form.get("description")
    goal_amount = request.form.get("goal")
    deadline = request.form.get("deadline")
    cause = Cause(
        name=name,
        description=description,
        goal_amount=goal_amount,
        deadline=deadline,
        user_id=user_id,
    )
    database.add(cause)
    # user posted a cause or sth
    return redirect(url_for("dashboard", user_id=user_id))


@app.route("/search-causes", methods=["POST", "GET"])
def search_causes():
    cause_name = unwrap(request.form.get("query"))
    cause_name_lower = cause_name.lower()
    all_causes = database.session.query(Cause).all()
    causes = [c.to_dict() for c in all_causes if cause_name_lower in c.name.lower()]
    data = {"results": causes}
    return success_response(data), 200


@app.route("/donate", methods=["POST"])
@login_required
def donate():
    user_id = request.form.get("user_id")
    cause_id = request.form.get("cause_id")
    amount_str = request.form.get("amount")
    amount = int(unwrap(amount_str))
    user = database.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return error_response(f"User with id{user_id} not found"), 404
    cause = database.session.query(Cause).filter_by(id=cause_id).first()
    if cause is None:
        return error_response(f"Cause with id {cause_id} not found"), 404
    # user_account_address = str(user.algo_account_address)
    # user_account_address = str(uuid4())
    # cause_account_address = str(cause.algo_account_address)
    # # To avoid the transaction failing incase account balance < amount + TRANSACTION_FEE
    # to_add = amount + algo.TRANSACTION_FEE
    # # We assume some fake bank transactions took place
    # algo.add_funds(to_add, user_account_address)
    # algo.donate(amount, user_account_address, cause_account_address)
    # new_balance = algo.get_balance(cause_account_address)
    # cause.current_amount = new_balance  # pyright: ignore
    # donation = Donation(cause_id=cause_id, user_id=user_id, amount=amount)
    # database.add(donation)
    # cause.update()
    # user.update()
    # donation_dict = donation.to_dict()
    return redirect(url_for("index"))


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
