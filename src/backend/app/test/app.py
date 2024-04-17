import requests
from pathlib import Path

# Define the URL of the Flask route
url = "http://localhost:5000/signup"
ROOT_DIR = Path(__file__).parent

def join_from_root(path: str) -> Path:
    return ROOT_DIR / path

def test_sign_up():
    data = {
        "first_name": "John",
        "second_name": "Doe",
        "email": "john@example.com",
        "algo_account_address": "ABC123",
    }

    files = {"profile_photo": open(join_from_root("profile_photo.jpg"))}
    response = requests.post(url, data=data, files=files)
    print("Response status code:", response.status_code)
    print("Response text:", response.text)

def test_login():
    pass
