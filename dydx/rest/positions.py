from typing import Any

from dydx.client import client
from dydx.parser import parse_positions


async def fetch_positions() -> dict[str, dict[str, Any]]:
    """
    Fetch the positions

    :returns: {market: {"market": market1, "size": size, "entry_price": entry_price}}
    """
    positions = await client.get(
        endpoint="v3/positions",
        container="positions",
    )
    print(positions)

    return parse_positions(positions)


async def fetch_position(market: str) -> dict[str, Any]:
    """
    Fetch the position for a given market
    """
    return (await fetch_positions()).get(market, {})
