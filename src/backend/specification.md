
# Backend Full Specification
***Warning: Each specification is subject to change*** 

# Database

## Entities

### 1. Donor
Represents a normal donating user.

| Column Name            | Data Type | Description                              |
|------------------------|-----------|------------------------------------------|
| id                     | int       | Unique identifier for the user.          |
| full_name              | string    | Full name of the user.                   |
| algo_account_id        | int       | Foreign key referencing the Algo Account table. |

### 2. Cause
A cause looking for donations.

| Column Name            | Data Type | Description                              |
|------------------------|-----------|------------------------------------------|
| id                     | int       | Unique identifier for the cause.         |
| name                   | string    | Name of the cause.                       |
| description            | string    | Description of the cause.                |
| algo_account_id        | int       | Foreign key referencing the Algo Account table. |
| smart_contract_id      | int       | Foreign key referencing the Smart Contract table. |

### 3. Smart Contract
Represents a smart contract that handles donations and funding for a cause.

| Column Name            | Data Type | Description                              |
|------------------------|-----------|------------------------------------------|
| id                     | int       | Unique identifier for the smart contract.|
| algo_account_id        | int       | Foreign key referencing the Algo Account table. |

### 4. Algo Account
Represents an Algorand account.

| Column Name            | Data Type | Description                              |
|------------------------|-----------|------------------------------------------|
| id                     | int       | Unique identifier for the Algo Account. |
| public_address         | string    | Public Algorand account address.         |
| private_address        | string    | Private Algorand account address.        |

# Algorand API

Specifies how the Algorand network will interact with the backend server and vice versa.

## create_new_account()

Creates a new Algorand account for a user/cause.

### Returns
- `public_address` (str): The newly generated public account address.
- `private_address` (str): The corresponding private account address.

## donate(cause_account, donor_account, amount)

Donate to a cause with a specified amount of Algos.

### Arguments
- `cause_account_public_address_address` (str): The public Algorand account address of the cause.
- `donor_account_private_address` (str): The private Algorand account address of the donor.
- `amount` (int): The amount of Algos to donate.

## get_amounts(cause_account_public_address)

Retrieve the current and goal donation amounts for a cause.

### Arguments
- `cause_account_public_address` (str): The public Algorand account address of the cause.

### Returns
- (int): The current donation amount in Algos.
- (int): The goal donation amount in Algos.

## fund(smart_contract_private_account_address)

Send current Algos in smart contract to cause's account. 

***Note: This is automatically called if current_amount reaches goal_amount.***

### Arguments
- `smart_contract_account_private_address` (str): The private Algorand account address of the smart contract.

# Backend API
- To be specified by whoever makes the backend server
