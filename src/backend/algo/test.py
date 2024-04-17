from .api import (
    TRANSACTION_FEE,
    create_account,
    add_funds,
    donate,
    get_balance,
    get_donations,
    MIN_ACC_BALANCE,
)
import pytest


def test_donate():
    donor = create_account()
    cause = create_account()
    donate_amt = 5000
    including_fee = donate_amt + TRANSACTION_FEE
    add_funds(including_fee, donor)
    donate(donate_amt, donor, cause)
    cause_balance = get_balance(cause)
    assert cause_balance == donate_amt, f"Expected {donate_amt}, got {cause_balance}"


def test_add_funds():
    donor = create_account()
    add_amt = 50_000
    add_funds(add_amt, donor)
    donor_balance = get_balance(donor)
    assert (
        donor_balance == MIN_ACC_BALANCE - add_amt
    ), f"Expected {MIN_ACC_BALANCE + add_amt}, got {donor_balance}"


def test_get_balance():
    acc = create_account()
    balance = get_balance(acc)
    assert balance == 0, f"Expected {MIN_ACC_BALANCE}, got {balance}"


@pytest.mark.skip("get_donations() still needs some work")
def test_get_donations():
    donor = create_account()
    cause = create_account()
    donate_amt = 69_000
    including_fee = donate_amt + TRANSACTION_FEE
    add_funds(including_fee, donor)
    donate(donate_amt, donor, cause)
    donations = get_donations(donor)
    __import__("pprint").pprint(donations)
    assert len(donations) == 1, f"Expected 1 donation, got {len(donations)}"
    assert (
        donations[0].amount == donate_amt
    ), f"Expected donation of {donate_amt}, got {donations[0].amount}"
    raise Exception()


def test_create_account():
    print("Testing create account")
    create_account()
