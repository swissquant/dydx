import asyncio
from dydx import WS_Order_Book


asyncio.run(WS_Order_Book(market="ETH-USD", silent=False).start())
