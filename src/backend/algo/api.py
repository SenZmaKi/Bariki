from dataclasses import dataclass
from typing import Any, cast
from algosdk import account, transaction
from algokit_utils import get_dispenser_account
from algosdk.constants import MIN_TXN_FEE
from beaker import localnet

ALGOD_CLIENT = localnet.get_algod_client()
INDEXER_CLIENT = localnet.get_indexer_client()
DISPENSER_ACCOUNT = get_dispenser_account(ALGOD_CLIENT)
MIN_ACC_BALANCE = 100_000
TRANSACTION_FEE = MIN_TXN_FEE
"""Algorand rejects any transactions that results in the account balance being below this"""


@dataclass
class Donation:
    donor_account_address: str
    account_cause_address: str
    amount: int


def _get_account(account_address: str) -> localnet.LocalAccount:
    accounts = localnet.get_accounts()
    for acc in accounts:
        if acc.address == account_address:
            return acc
    raise ValueError(f"Failed to find {account_address} in localnet")


def _make_transaction(
    amt: int,
    sender_sk: str,
    sender_address: str,
    receiver_address: str,
    sp: transaction.SuggestedParams,
) -> None:
    balance = get_balance(sender_address, True)
    full_spend = amt + TRANSACTION_FEE
    new_balance = balance - full_spend
    if new_balance < MIN_ACC_BALANCE:
        raise Exception(
            f"""Transaction + Transaction fee results in a balance below the minimum account balance i.e., 
            {amt} + {TRANSACTION_FEE} = {full_spend}
            {balance} - {full_spend} = {new_balance}
            {new_balance} < {MIN_ACC_BALANCE}"""
        )

    unsigned_txn = transaction.PaymentTxn(
        sender=sender_address,
        receiver=receiver_address,
        amt=amt,
        sp=sp,
    )
    signed_txn = unsigned_txn.sign(sender_sk)
    txid = ALGOD_CLIENT.send_transaction(signed_txn)
    transaction.wait_for_confirmation(ALGOD_CLIENT, txid)


def donate(amt: int, donor_account_address: str, cause_account_address: str) -> None:
    """
    Donate into the cause account address
    """
    sender_acc = _get_account(donor_account_address)
    _make_transaction(
        amt,
        sender_acc.private_key,
        sender_acc.address,
        cause_account_address,
        ALGOD_CLIENT.suggested_params(),
    )


def fund(amount: int, cause_account_address: str, user_account_address: str):
    """
    Fund the user once the goal is reached/deadline has expired
    """
    acc = _get_account(cause_account_address)
    _make_transaction(
        amount,
        acc.private_key,
        acc.address,
        user_account_address,
        ALGOD_CLIENT.suggested_params(),
    )


def add_funds(amount: int, user_account_address: str) -> None:
    """
    Load funds into the donor's account
    """
    sp = ALGOD_CLIENT.suggested_params()
    _make_transaction(
        amount,
        DISPENSER_ACCOUNT.private_key,
        DISPENSER_ACCOUNT.address,
        user_account_address,
        sp=sp,
    )


def get_balance(account_address: str, get_real_balance=False) -> int:
    """
    Get the account's balance
    :param: get_real_balance: boolean indicating whether to not subtract minimum account balance from the real balance, leave as `False` if you don't understand
    """
    resp = cast(dict[str, Any], ALGOD_CLIENT.account_info(account_address))
    real_balance = resp["amount"]
    if get_real_balance:
        return real_balance
    balance = real_balance - MIN_ACC_BALANCE
    return balance


def create_account() -> str:
    """
    Create an account for a cause/donor
    :return: account address
    """
    private_key, account_address = account.generate_account()
    localnet.add_account(private_key)
    add_funds(MIN_ACC_BALANCE, account_address)
    return account_address
