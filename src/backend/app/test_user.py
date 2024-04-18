#!/usr/bin/python3
""" Test db """
from models.user import User
from models import database


def test_create_user():
    new_user = User(first_name='giga',
                    second_name='chad',
                    email='gogo@gmail.com',
                    algo_account_address='randomstring',
                    hashed_password='sdfefrefrer',
                    bank_creds=None,
                    profile_pic_url=None
                    )
    user_id = new_user.id
    try:
        database.add(new_user)
    except Exception as e:
        print(f"Error creating user {e}")
    else:
        print(f"User created successfully {user_id}")
    return user_id

def test_get_user(u_id: str):
    try:
        user = database.get(User, u_id)
    except Exception as e:
        print(f"An error occured while getting user {u_id}  {e}")
    else:
        print("User fetched successfully..")
        print(user.to_dict())

def get_all_users():
    all_users = database.all(User)
    users = list()
    for u in all_users:
        obj_id = u.split(".")[1]
        obj = database.get(User, obj_id)
        users.append(obj.to_dict())
    return users

def get_user_donations():

if __name__ == "__main__":
    u_id = test_create_user()
    test_get_user(u_id)
    print()
    print("--------")
    print("All users")
    print(get_all_users())
    # database.flush_database()
