import asyncio

from rest import fetch_markets


lock = asyncio.Lock()


class Markets:
    def __init__(self):
        self.initialised = asyncio.Event()
        self.cache: dict[str, dict] = None

    def __getitem__(self, ticker: str):
        return self.cache[ticker]

    async def initialise(self):
        """
        Fetch and store the market descriptions in the cache
        """
        async with lock:
            if not self.initialised.is_set():
                self.cache = await fetch_markets()
                self.initialised.set()


markets = Markets()
