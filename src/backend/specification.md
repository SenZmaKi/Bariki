# Backend Full Specification
***Warning: Each specification is subject to change*** 

## Database

### Models

#### 1. User
Represents a normal user.

| Column Name          | Data Type | Description                              |
|----------------------|-----------|------------------------------------------|
| id                   | int       | Unique identifier for the user.          |
| full_name            | string    | Full name of the user.                   |
| profile_photo_url    | string    | URL of the user's profile photo.         |
| algo_account_address | string    | Algorand account address of the user.    |
| bank_credentials     | string    | Bank credentials e.g., visa card, master card etc., |
| causes               | Foreign Key | References the causes the user has started. |
| donations            | Foreign Key | References the donations made by the user. |

#### 2. Cause
Represents a created cause looking for donations.

| Column Name      | Data Type | Description                                |
|------------------|-----------|--------------------------------------------|
| id               | int       | Unique identifier for the cause.           |
| name             | string    | Name of the cause.                         |
| description      | string    | Description of the cause.                  |
| image_url        | string    | URL of an image representing the cause.    |
| current_amount   | int       | Current amount of donations for the cause. |
| goal_amount      | int       | Goal amount of donations for the cause.    |
| deadline         | date      | Deadline for the cause.                    |
| algo_account_id  | int       | Algorand account ID associated with the cause. |
| donations        | Foreign Key | References the donations made to the cause. |
| is_ongoing       | bool      | Indicates if the cause is ongoing or not.  |

#### 3. Donation
Represents a donation made by a user to a cause.

| Column Name | Data Type | Description                            |
|-------------|-----------|----------------------------------------|
| id          | int       | Unique identifier for the donation.    |
| amount      | int       | Amount of the donation.                |
| user        | Foreign Key | References the user who made the donation. |
| cause       | Foreign Key | References the cause the donation is for.   |

---

With these changes, the `causes` and `donations` fields in the `User` model, and the `user` and `cause` fields in the `Donation` model are now properly defined as foreign key references to their respective models. Let me know if you need further adjustments or additional information!

## Algorand API

#### donate
Donates a specified amount from the donor's account to the cause's account.

- Parameters:
  - `amt` (int): The amount to donate.
  - `donor_account_address` (str): The address of the donor's account.
  - `cause_account_address` (str): The address of the cause's account.
  
- Returns: None

#### add_funds
Loads funds into the donor's account.

- Parameters:
  - `amount` (int): The amount of funds to add.
  - `donor_account_address` (str): The address of the donor's account.

- Returns: None

#### get_balance
Gets the balance of the specified account.

- Parameters:
  - `account_address` (str): The address of the account.
  - `get_real_balance` (bool): A boolean indicating whether not to subtract the minimum account balance from the real balance. Default is `False`.

- Returns: int - The account balance.

#### create_account
Creates an account for a cause or donor.

- Returns: str - The address of the newly created account.

## Controller/Router specification
***TODO***

