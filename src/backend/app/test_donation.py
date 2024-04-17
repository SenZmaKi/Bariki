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


def test_create_donation():
    # make sure there's at least one user
    sample_user_id = db.get(User, _id(list(db.all(User).keys())[0])).id
    sample_cause_id = db.get(Cause, _id(list(db.all(Cause).keys())[0])).id
    new_donation = Donation(amount=100,
                     cause_id=sample_cause_id,
                     user_id=sample_user_id
                    )
    don_id = new_donation.id
    try:
        db.add(new_donation)
    except Exception as e:
        print(f"Error creating user {e}")
    else:
        print(f"Donation created successfully {don_id}")
    return don_id

def test_get_donation(u_id: str):
    try:
        donation = db.get(Donation, u_id)
    except Exception as e:
        print(f"An error occured while getting donation {u_id}  {e}")
    else:
        print("Donation fetched successfully..")
        print(donation.to_dict())

def test_get_all_donations():
    all_dons = db.all(Donation)
    donations = list()
    for u in all_dons:
        obj_id = _id(u)
        obj = db.get(Donation, obj_id)
        donations.append(obj.to_dict())
    return donations

if __name__ == "__main__":
    u_id = test_create_donation()
    test_get_donation(u_id)
    print()
    print("--------")
    print("All donations"
    print(test_get_all_donations())
    # db.flush_database()
