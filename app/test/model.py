from app.models.base import get_current_utc_time
from app.models.user import User
from app.models.cause import Cause
from app.models import database
from pprint import pprint


def test_create_user():
    user = User(
        first_name="giga",
        second_name="chad",
        hashed_password="somecrap",
        email="gogo@gmail.com",
    )
    database.add(user)
    pprint(user.to_dict())
    return user


def test_create_cause():
    cause = Cause(
        name="Get Lelei Chuja",
        description="Lelei's shoes have seen decades on this tarmac, please let them rest in peace by getting him new ones",
        image_url="cause_image_url.jpg",
        goal_amount=69420,
        deadline=get_current_utc_time(),
    )
    database.add(cause)
    pprint(cause.to_dict())
    return cause
