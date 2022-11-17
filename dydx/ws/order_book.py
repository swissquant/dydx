from .client import WS

from link import pubsub

from dydx.parser import parse_order_book


class WS_Order_Book(WS):
    def __init__(self, market: str, silent: bool = True):
        self.market = market
        self.silent = silent

    def parse(self, quotes):
        """
        Parse the raw quotes from DYDX
        """
        _quotes = {}
        for quote in quotes:
            # Trying this format that happens after initial message
            try:
                _quotes[float(quote[0])] = float(quote[1])
            # If not working, it's because it's the initial message
            # Therefore, using this format
            except Exception:
                _quotes[float(quote["price"])] = float(quote["size"])

        return _quotes

    async def start(self):
        await self.connect()
        await self.subscribe(channel="v3_orderbook", id=self.market)

        while True:
            order_book = await self.receive()
            pubsub.send(topic="dydx:order_book", message=parse_order_book(order_book), silent=self.silent)
