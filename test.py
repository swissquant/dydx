import asyncio
from dydx import fetch_positions


print(asyncio.run(fetch_positions()))
