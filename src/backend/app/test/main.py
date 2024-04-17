import requests
from app.models.cause import Cause
from app.test.mock import CREATE_CAUSE_DTO, USER_LOGIN_DTO, USER_SIGNUP_DTO
from app.test.utils import join_from_root
from app.test import model as test_model
from app.models import database


def make_url(resource: str) -> str:
    url = f"http://localhost:5000/{resource}"
    return url


class TestFailedException(Exception):
    def __init__(self) -> None:
        super().__init__("Test failed")


def print_response(response: requests.Response) -> None:
    print("Response status code:", response.status_code)
    print("Response text:", response.text)


def test_sign_up():
    pfp_path = join_from_root("profile_photo.jpg")
    with open(pfp_path) as pfp:
        files = {"profile_photo": pfp}
        url = make_url("signup")
        response = requests.post(url, data=USER_SIGNUP_DTO, files=files)
        print_response(response)
        if response.status_code != 200 or response.status_code != 409:
            raise TestFailedException()


def test_login():
    url = make_url("login")
    response = requests.post(url, data=USER_LOGIN_DTO)
    print_response(response)
    if response.status_code != 200:
        raise TestFailedException()


def test_create_cause():
    url = make_url("create-cause")
    response = requests.post(url, data=CREATE_CAUSE_DTO)
    print_response(response)
    if response.status_code != 201:
        raise TestFailedException()


def test_donate():
    user = test_model.test_create_user()
    cause = test_model.test_create_cause()
    url = make_url("donate")
    amount = 69420
    data = {"user_id": user.id, "cause_id": cause.id, "amount": amount}
    response = requests.post(url, data=data)
    print_response(response)
    if response.status_code != 201:
        raise TestFailedException()


def test_search_causes():
    cause = test_model.test_create_cause()
    url = make_url("search-causes")
    data = {"query": cause.name}
    response = requests.post(url, data)
    print_response(response)
    resp_json = response.json()
    causes = resp_json["data"]["results"]
    if response.status_code != 200 or not any(c["id"] == cause.id for c in causes):
        raise TestFailedException()


test_donate()
