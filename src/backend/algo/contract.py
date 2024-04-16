from beaker import LocalStateValue
from beaker.application import (
    Application,
    unconditional_create_approval,
    unconditional_opt_in_approval,
)
from pyteal import Expr, TealType, Int, abi


class LocalState:
    goal_amount = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Cause goal amount",
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
