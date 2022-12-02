from dydx.parser import parse_account
from dydx.client import client, client_priv
from dydx3.helpers.db import get_account_id


async def fetch_account(client=client, client_priv=client_priv):
    account_id = get_account_id(address=client_priv.private.default_address)
    account = await client.get(
        endpoint=f"v3/accounts/{account_id}",
        container="account",
    )

    return parse_account(account)
