import asyncio
from dydx import WS_Order_Book


print(asyncio.run(WS_Order_Book(market="ETH-USD", silent=False).start()))
