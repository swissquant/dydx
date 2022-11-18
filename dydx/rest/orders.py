import time
from typing import Optional

from dydx3.starkex.order import SignableOrder
from dydx3.helpers.request_helpers import random_client_id

from dydx.markets import markets
from dydx.helpers import timestamp_to_iso
from dydx.rest.account import fetch_account
from dydx.client import client, client_priv, rate_limits


position_id = ""


async def create_order(
    ticker: str,
    order_type: str,
    size: float,
    price: float,
    post_only: bool = False,
    time_in_force: str = "FOK",
) -> dict:
    """
    Create an order
    """
    global position_id

    # Determining the size
    if size > 0:
        side = "BUY"
    else:
        side = "SELL"

    # Fetching the position id
    if position_id == "":
        account = await fetch_account()
        position_id = account["position_id"]

    # Signing the order with the stark key
    client_id = random_client_id()
    expiration = time.time() + 5 * 60
    order_to_sign = SignableOrder(
        network_id=client_priv.network_id,
        position_id=position_id,
        client_id=client_id,
        market=ticker,
        side=side,
        human_size=str(abs(size)),
        human_price=str(price),
        limit_fee="0.1",
        expiration_epoch_seconds=expiration,
    )
    order_signature = order_to_sign.sign(private_key_hex=client_priv.stark_private_key)

    # Creating the order
    status = await client.post(
        endpoint="v3/orders",
        container="order",
        market=ticker,
        side=side,
        type=order_type,
        postOnly=post_only,
        size=str(abs(size)),
        price=str(price),
        limitFee="0.1",
        expiration=timestamp_to_iso(timestamp=expiration),
        timeInForce=time_in_force,
        clientId=client_id,
        signature=order_signature,
    )

    return status


async def create_market_order(ticker: str, size: float, price: Optional[float] = None) -> dict:
    """
    Create a market order of a given size on the given ticker
    """
    # Fetching the markets
    await markets.initialise()

    # Assigning the work price if not filled
    if price is None:
        if size > 0:
            price = 1000000000
        else:
            price = float(markets.cache[ticker]["tickSize"])

    # Throttling
    await rate_limits["market_orders"][ticker].throttle()

    # Creating the order
    status = await create_order(
        ticker=ticker,
        order_type="MARKET",
        size=size,
        price=round(price, 10),
        time_in_force="FOK",
    )

    return status


async def create_limit_order(ticker: str, size: float, price: float) -> dict:
    """
    Create a limit order of a given size on the given ticker
    """
    await rate_limits["limit_orders"][ticker].throttle()
    status = await create_order(
        ticker=ticker,
        order_type="LIMIT",
        size=size,
        price=price,
        time_in_force="GTT",
    )

    return status
