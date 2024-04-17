import requests
from pathlib import Path

# Define the URL of the Flask route
ROOT_DIR = Path(__file__).parent


def make_url(resource: str) -> str:
    url = f"http://localhost:5000/{resource}"
    return url


def join_from_root(path: str) -> Path:
    return ROOT_DIR / path


MOCK_USER = {
    "first_name": "John",
    "second_name": "Doe",
    "email": "john@example.com",
    "password": "1234",
}


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
        response = requests.post(url, data=MOCK_USER, files=files)
        print_response(response)
        if response.status_code != 200 or response.status_code != 409:
            raise TestFailedException()


def test_login():
    data = {"email": MOCK_USER["email"], "password": MOCK_USER["password"]}
    url = make_url("login")
    response = requests.post(url, data=data)
    print_response(response)
    if response.status_code != 200:
        raise TestFailedException()
