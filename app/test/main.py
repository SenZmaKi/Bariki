import requests
from app.test.mock import CREATE_CAUSE_DTO, DONATE_DTO, USER_LOGIN_DTO, USER_SIGNUP_DTO
from app.test.utils import join_from_root
from app.test import model as test_model


def make_url(resource: str) -> str:
    url = f"http://localhost:5000/{resource}"
    return url


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
        assert response.status_code == 200 or response.status_code == 409


def test_login():
    url = make_url("login")
    response = requests.post(url, data=USER_LOGIN_DTO)
    print_response(response)
    assert response.status_code != 200


def test_create_cause():
    user = test_model.test_create_user()
    url = make_url("create-cause")
    data = CREATE_CAUSE_DTO.copy()
    data["user_id"] = user.id
    response = requests.post(url, data)
    print_response(response)
    assert response.status_code == 201


def test_donate():
    user = test_model.test_create_user()
    cause = test_model.test_create_cause()
    url = make_url("donate")
    data = DONATE_DTO.copy()
    data["user_id"] = user.id
    data["cause_id"] = cause.id
    response = requests.post(url, data=data)
    print_response(response)
    assert response.status_code == 201


def test_search_causes():
    cause = test_model.test_create_cause()
    url = make_url("search-causes")
    data = {"query": cause.name}
    response = requests.post(url, data)
    print_response(response)
    resp_json = response.json()
    assert response.status_code == 200
    causes = resp_json["data"]["results"]
    assert any(c["id"] == cause.id for c in causes)


def test_get_causes():
    cause = test_model.test_create_cause()
    url = make_url("causes")
    response = requests.get(url)
    print_response(response)
    assert response.status_code == 200
    resp_json = response.json()
    causes = resp_json["data"]["causes"]
    assert any(c["id"] == cause.id for c in causes)
