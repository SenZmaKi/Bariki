#!/usr/bin/python3
""" Test db """
from models.user import User
from models.cause import Cause
from models.donation import Donation
from models import database as db
from datetime import datetime, timedelta


def _id(obj_id: str) -> str:
    """ Returns object id from full instance id
        NB: instance id is returned as <CLASS>.<instance_id> from db.all()
    """
    return obj_id.split(".")[1]


def test_create_cause():
    # make sure there's at least one user
    sample_user_id = db.get(User, _id(list(db.all(User).keys())[0])).id
    new_cause = Cause(name='changisha for giga again',
                    description='changishia for giga to get school fees once again',
                    image_url=None,
                    goal_amount=5000,
                    deadline=(datetime.now() + timedelta(days=1)),
                    algo_account_address='randomstring23dwe',
                    bank_creds=None,
                    user_id=sample_user_id,
                    profile_pic_url=None
                    )
    cause_id = new_cause.id
    try:
        db.add(new_cause)
    except Exception as e:
        print(f"Error creating user {e}")
    else:
        print(f"Cause created successfully {cause_id}")
        print(db.get(Cause, cause_id))
    return cause_id

def test_get_cause(u_id: str):
    try:
        cause = db.get(Cause, u_id)
    except Exception as e:
        print(f"An error occured while getting cause {u_id}  {e}")
    else:
        print("Cause fetched successfully..")
        print(cause.to_dict())

def test_get_all_causes():
    all_causes = db.all(Cause)
    causes = list()
    for u in all_causes:
        obj_id = _id(u)
        obj = db.get(Cause, obj_id)
        causes.append(obj.to_dict())
    return causes

if __name__ == "__main__":
    u_id = test_create_cause()
    test_get_cause(u_id)
    print()
    print("-------")
    print("All causes")
    print(test_get_all_causes())
    # db.flush_database()
