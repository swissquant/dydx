from dydx.client import client


async def fetch_markets():
    """
    Fetch the metadata of the markets
    """
    markets = await client.get(endpoint="v3/markets", container="markets")

    return markets
