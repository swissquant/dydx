import asyncio
from dydx import create_limit_order


asyncio.run(create_limit_order(market="ETH-USD", size=-0.01, price=9000))
