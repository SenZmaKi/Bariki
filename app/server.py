#!/usr/bin/python3
"""App main module (controller and service)"""

import os
from pathlib import Path
from typing import Any, TypeVar, cast
from flask import Response, jsonify, Flask, request
from flask.templating import render_template
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import database
from app.models.donation import Donation
from app.models.user import User
from app.models.cause import Cause
from app import algo

ROOT_DIR = Path(__file__).parent
UPLOAD_FOLDER = ROOT_DIR / "uploads"
if not UPLOAD_FOLDER.is_dir():
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)

T = TypeVar("T")


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
    causes = database.session.query(Cause).all()
    return render_template("index.html")

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
    password = unwrap(request.form.get("password"))
    target_users = [
        u
        for u in users
        if check_password_hash(u.hashed_password, password)  # pyright: ignore
    ]
    if not target_users:
        return error_response("Invalid password"), 401
    user_dict = target_users[0].to_dict()
    return user_dict, 200


@app.route("/causes", methods=["GET"])
def causes():
    all_causes = database.session.query(Cause).all()
    all_causes_dict = [c.to_dict() for c in all_causes]
    data = {"causes": all_causes_dict}
    return success_response(data), 200


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
    user = User(
        first_name=first_name,
        second_name=second_name,
        hashed_password=hashed_password,
        email=email,
        profile_pic_url=profile_pic_url,
    )
    # Add the new_user to the database session
    database.add(user)
    user_dict = user.to_dict()
    return success_response(user_dict), 201


@app.route("/create-cause", methods=["POST"])
def create_cause():
    name = request.form.get("name")
    description = request.form.get("description")
    goal_amount = request.form.get("goal_amount")
    deadline = request.form.get("deadline")
    user_id = request.form.get("user_id")
    cause = Cause(
        name=name,
        description=description,
        goal_amount=goal_amount,
        deadline=deadline,
        user_id=user_id,
    )
    database.add(cause)
    cause_dict = cause.to_dict()
    return success_response(cause_dict), 201


@app.route("/search-causes", methods=["POST"])
def search_causes():
    cause_name = unwrap(request.form.get("query"))
    cause_name_lower = cause_name.lower()
    all_causes = database.session.query(Cause).all()
    causes = [c.to_dict() for c in all_causes if cause_name_lower in c.name.lower()]
    data = {"results": causes}
    return success_response(data), 200


@app.route("/donate", methods=["POST"])
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
    user_account_address = str(user.algo_account_address)
    cause_account_address = str(cause.algo_account_address)
    # To avoid the transaction failing incase account balance < amount + TRANSACTION_FEE
    to_add = amount + algo.TRANSACTION_FEE
    # We assume some fake bank transactions took place
    algo.add_funds(to_add, user_account_address)
    algo.donate(amount, user_account_address, cause_account_address)
    new_balance = algo.get_balance(cause_account_address)
    cause.current_amount = new_balance  # pyright: ignore
    donation = Donation(cause_id=cause_id, user_id=user_id, amount=amount)
    database.add(donation)
    cause.update()
    user.update()
    donation_dict = donation.to_dict()
    return success_response(donation_dict), 201


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
