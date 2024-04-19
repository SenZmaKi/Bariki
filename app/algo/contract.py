from algokit_utils import ApplicationClient
from beaker import LocalStateValue
from beaker.application import (
    Application,
    unconditional_create_approval,
    unconditional_opt_in_approval,
)
from pyteal import Expr, TealType, Int, abi
from . import api


class LocalState:
    goal_amount = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Cause goal amount",
    )
    current_amount = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Current  amount",
    )


app = (
    Application("Bariki", state=LocalState())
    .apply(unconditional_create_approval)
    .apply(unconditional_opt_in_approval)
)


@app.external
def get_goal_amount(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.goal_amount)


@app.external
def set_goal_amount(amt: abi.Uint64) -> Expr:
    return app.state.goal_amount.set(amt.get())


@app.external
def get_current_amount(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.current_amount)


@app.external
def set_current_amount(amt: abi.Uint64) -> Expr:
    return app.state.current_amount.set(amt.get())


def update_balance(
    donor_addresss: str, app_client: ApplicationClient, amt: int
) -> None:
    goal_amt = app_client.call("get_goal_amount").return_value
    donor = api._get_account(donor_addresss)
    api._make_transaction(
        amt,
        donor.private_key,
        donor.address,
        app_client.app_address,
        app_client.suggested_params,  # pyright: ignore
    )
    current_amt = app_client.call("get_current_amount").return_value
    if current_amt > goal_amt:
        api._make_transaction(
            current_amt,
            app_client.app_address,
            app_client.signer,
            donor.private_key,
            app_client.sender,
            app_client.suggested_params,  # pyright: ignore
        )
