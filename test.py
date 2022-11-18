import asyncio
from dydx import create_market_order


asyncio.run(create_market_order(market="ETH-USD", size=-0.01))
