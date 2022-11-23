import asyncio
from dydx import WS_Account


print(asyncio.run(WS_Account().start()))
