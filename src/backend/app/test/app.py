import requests
from pathlib import Path

# Define the URL of the Flask route
url = "http://localhost:5000/signup"
ROOT_DIR = Path(__file__).parent
join_from_root = lambda p: ROOT_DIR.joinpath(p)

# Define the data to be sent in the request
data = {
    "first_name": "John",
    "second_name": "Doe",
    "email": "john@example.com",
    "algo_account_address": "ABC123",
}

# Define the files to be sent in the request (profile photo)
files = {"profile_photo": open(join_from_root("profile_photo.jpg"))}

# Make the POST request
response = requests.post(url, data=data, files=files)

# Print the response status code
print("Response status code:", response.status_code)
