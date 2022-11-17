def format(_account: dict) -> dict:
    account = {
        "balance": float(_account["equity"]),
        "free_collateral": float(_account["freeCollateral"]),
        "position_id": _account["positionId"],
        "account_number": _account["accountNumber"],
    }
    return account
