from typing import NamedTuple, cast
from algosdk import account, transaction
from beaker import localnet
from beaker.client import ApplicationClient
from .contract import app
from . import contract

ALGOD_CLIENT = localnet.get_algod_client()
INDEXER_CLIENT = localnet.get_indexer_client()
app.build().export("./artifacts")


def _get_app_client(account_address: str):
    acc = _find_account(account_address)
    return ApplicationClient(
        client=ALGOD_CLIENT,
        app=app,
        sender=acc.address,
        signer=acc.signer,
    )


def _find_account(account_address: str):
    accounts = localnet.get_accounts()
    for acc in accounts:
        if acc.address == account_address:
            return acc
    raise ValueError(f"Failed to find {account_address} in localnet")


def _create_new_account() -> str:
    private_key, account_address = account.generate_account()
    localnet.add_account(private_key)
    return account_address


def create_new_cause_account(goal_amount: int):
    _, account_address = _create_new_account()
    app_client = cast(ApplicationClient, _get_app_client(account_address))
    app_client.create()
    app_client.opt_in()
    app_client.call(contract.set_goal_amount, amt=goal_amount)
    return account_address


def create_new_donor_account():
    return _create_new_account()


class Amounts(NamedTuple):
    goal_amount: int
    current_amount: int


def get_current_amount(smart_contract_address: str) -> int:
    app_client = _get_app_client(smart_contract_address)
    info = app_client.get_application_account_info()
    balance = info["amount"]
    current_amount = balance - info.get("min_balance")
    return current_amount


def get_goal_amount(smart_contract_address: str) -> int:
    app_client = _get_app_client(smart_contract_address)
    goal_amount = app_client.call(contract.get_goal_amount).return_value
    return goal_amount


def _make_transaction(
    amt: int,
    sender_sk: str,
    sender_address: str,
    receiver_address: str,
    sp: transaction.SuggestedParams,
):
    unsigned_txn = transaction.PaymentTxn(
        sender=sender_address,
        receiver=receiver_address,
        amt=amt,
        sp=sp,
    )
    signed_txn = unsigned_txn.sign(sender_sk)
    txid = ALGOD_CLIENT.send_transaction(signed_txn)
    transaction.wait_for_confirmation(ALGOD_CLIENT, txid)


def donate(amt: int, donor_account_address: str, smart_contract_address: str) -> bool:
    """
    :returns: Boolean indicating whether this donation achieved the goal amount i.e., if `True`, goal reach else not reached
    """
    app_client = _get_app_client(smart_contract_address)
    sender_acc = _find_account(donor_account_address)
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


def fund(smart_contract_address: str) -> None:
    app_client = _get_app_client(smart_contract_address)
    amt = get_current_amount(smart_contract_address)
    app_client.fund(amt)
