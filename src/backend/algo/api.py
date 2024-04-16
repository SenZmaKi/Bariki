from dataclasses import dataclass
from typing import cast
from algosdk import account, transaction
from algokit_utils import get_dispenser_account
from beaker import localnet
from beaker.client import ApplicationClient
from .contract import app
from . import contract

ALGOD_CLIENT = localnet.get_algod_client()
INDEXER_CLIENT = localnet.get_indexer_client()
DISPENSER_ACCOUNT = get_dispenser_account(ALGOD_CLIENT)
app.build().export("./artifacts")


@dataclass
class Donation:
    donor_address: str
    smart_contract_address: str
    amount: int


def _get_app_client(account_address: str) -> ApplicationClient:
    acc = _get_account(account_address)
    return ApplicationClient(
        client=ALGOD_CLIENT,
        app=app,
        sender=acc.address,
        signer=acc.signer,
    )


def _get_account(account_address: str) -> localnet.LocalAccount:
    accounts = localnet.get_accounts()
    for acc in accounts:
        if acc.address == account_address:
            return acc
    raise ValueError(f"Failed to find {account_address} in localnet")


def _create_new_account() -> str:
    private_key, account_address = account.generate_account()
    localnet.add_account(private_key)
    return account_address


def _make_transaction(
    amt: int,
    sender_sk: str,
    sender_address: str,
    receiver_address: str,
    sp: transaction.SuggestedParams,
) -> None:
    unsigned_txn = transaction.PaymentTxn(
        sender=sender_address,
        receiver=receiver_address,
        amt=amt,
        sp=sp,
    )
    signed_txn = unsigned_txn.sign(sender_sk)
    txid = ALGOD_CLIENT.send_transaction(signed_txn)
    transaction.wait_for_confirmation(ALGOD_CLIENT, txid)


def create_new_cause_account(goal_amount: int) -> str:
    """
    Create a new account for a cause
    :returns: The account address
    """
    _, account_address = _create_new_account()
    app_client = cast(ApplicationClient, _get_app_client(account_address))
    app_client.create()
    app_client.opt_in()
    app_client.call(contract.set_goal_amount, amt=goal_amount)
    return account_address


def create_new_donor_account() -> str:
    """
    Create a new account for a donator
    :returns: The account address
    """
    account_address = _create_new_account()
    return account_address


def get_current_amount(smart_contract_address: str) -> int:
    """
    Get the current amount that the cause has raised
    """
    app_client = _get_app_client(smart_contract_address)
    info = app_client.get_application_account_info()
    balance = info["amount"]
    current_amount = balance - info.get("min_balance")
    return current_amount


def get_goal_amount(smart_contract_address: str) -> int:
    """
    Get the target goal amount for the cause
    """
    app_client = _get_app_client(smart_contract_address)
    goal_amount = app_client.call(contract.get_goal_amount).return_value
    return goal_amount


def donate(amt: int, donor_account_address: str, smart_contract_address: str) -> bool:
    """
    Donate into the smart contract account
    :returns: Boolean indicating whether this donation achieved the goal amount i.e., if `True`, goal reached else not reached
    """
    app_client = _get_app_client(smart_contract_address)
    sender_acc = _get_account(donor_account_address)
    goal_amt = get_goal_amount(smart_contract_address)
    _make_transaction(
        amt,
        sender_acc.private_key,
        sender_acc.address,
        smart_contract_address,
        sp=app_client.get_suggested_params(),
    )
    current_amt = get_current_amount(smart_contract_address)
    if current_amt >= goal_amt:
        fund(smart_contract_address)
        return True
    return False


def add_funds(amount: int, donor_account_address: str) -> None:
    """
    Load funds into the donor's account
    """
    _make_transaction(
        amount,
        DISPENSER_ACCOUNT.private_key,
        DISPENSER_ACCOUNT.address,
        donor_account_address,
        ALGOD_CLIENT.suggested_params(),
    )


def get_balance(donor_account_address: str) -> int:
    """
    Get the donor's account balance
    """
    info = INDEXER_CLIENT.account_info(donor_account_address)
    balance = info["amt"] - info["min_balance"]
    return balance


def fund(smart_contract_address: str) -> None:
    """
    Release all funds currently held in the smart contract's account into the cause's account
    - Note: This is automatically invoked during a donation when the donation reaches the goal amount
    """
    app_client = _get_app_client(smart_contract_address)
    amt = get_current_amount(smart_contract_address)
    app_client.fund(amt)


def get_donations(donor_account_address: str) -> list[Donation]:
    """
    Retrieve all donations made by the donor
    """
    txns = INDEXER_CLIENT.search_transactions(
        address=donor_account_address, address_role="sender"
    )
    donations = [Donation(txn["snd"], txn["rcx"], txn["amt"]) for txn in txns]
    return donations
