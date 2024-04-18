from app.models.base import get_current_utc_time


CREATE_CAUSE_DTO = {
    "name": "Get Lelei Chuja",
    "description": "Lelei's shoes have seen decades on this tarmac, please let them rest in peace by getting him new ones",
    "image_url": "cause_image_url.jpg",
    "goal_amount": 69420,
    "deadline": get_current_utc_time().isoformat(),
    "user_id": "",
}

USER_SIGNUP_DTO = {
    "first_name": "Giga",
    "second_name": "Chad",
    "hashed_password": "somecrap!2315&",
    "email": "gogo@gmail.com",
}

USER_LOGIN_DTO = {
    "email": USER_SIGNUP_DTO["email"],
    "hashed_password": USER_SIGNUP_DTO["hashed_password"],
}

DONATE_DTO = {"cause_id": "", "user_id": "", "amount": 69420}
