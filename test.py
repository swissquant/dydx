import asyncio
from dydx import WS_Trades


asyncio.run(WS_Trades(market="BTC-USD").start())
