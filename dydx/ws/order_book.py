from .client import WS

from link import pubsub

from dydx.parser import parse_order_book


class WS_Order_Book(WS):
    def __init__(self, market: str, silent: bool = True):
        self.market = market
        self.silent = silent
        self.order_book: dict[str, dict[float, float]] = {"bids": {}, "asks": {}}

    def update_quotes(self, bids: list[list[str]], asks: list[list[str]]):
        for quote in bids:
            self.order_book["bids"][float(quote[0])] = float(quote[1])

        for quote in asks:
            self.order_book["asks"][float(quote[0])] = float(quote[1])

    def order_quotes(self):
        self.order_book["bids"] = dict(sorted(self.order_book["bids"].items(), reverse=True))
        self.order_book["asks"] = dict(sorted(self.order_book["asks"].items()))

    async def start(self):
        await self.connect()
        await self.subscribe(channel="v3_orderbook", id=self.market)

        while True:
            order_book = await self.receive()

            # The first message contains the full order book
            # All the other messages only contain the updates
            match order_book:
                # Updates
                case {"offset": _, "bids": bids, "asks": asks}:
                    self.update_quotes(bids, asks)
                # First message
                case {"bids": _, "asks": _}:
                    self.order_book = parse_order_book(order_book)

            self.order_quotes()
            pubsub.send(topic="dydx:order_book", message=self.order_book, silent=self.silent)
