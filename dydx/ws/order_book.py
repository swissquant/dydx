from .client import WS

from link import pubsub

from dydx.parser import parse_order_book
from dydx.helpers import restart_on_failure


class WS_Order_Book(WS):

    topic = "dydx:order_book"

    def __init__(self, market: str, silent: bool = True):
        self.market = market
        self.silent = silent
        self.order_book: dict[str, dict[str, dict[float, float]]]

    def update_quote(self, side: str, quote: list[str], offset: float):
        price = float(quote[0])
        if offset > self.order_book["offsets"][side].get(price, 0):
            self.order_book["quotes"][side][price] = float(quote[1])
            self.order_book["offsets"][side][price] = offset

    def update_quotes(self, bids: list[list[str]], asks: list[list[str]], offset: str):
        for quote in bids:
            self.update_quote(side="bids", quote=quote, offset=float(offset))

        for quote in asks:
            self.update_quote(side="asks", quote=quote, offset=float(offset))

    def order_quotes(self):
        self.order_book["quotes"]["bids"] = dict(sorted(self.order_book["quotes"]["bids"].items(), reverse=True))
        self.order_book["quotes"]["asks"] = dict(sorted(self.order_book["quotes"]["asks"].items()))

    @restart_on_failure
    async def start(self):
        await self.connect()
        await self.subscribe(channel="v3_orderbook", id=self.market, includeOffsets=True)

        while True:
            order_book = await self.receive()
            # The first message contains the full order book
            # All the other messages only contain the updates
            match order_book:
                # Updates
                case {"offset": offset, "bids": bids, "asks": asks}:
                    self.update_quotes(bids, asks, offset)
                # First message
                case {"bids": _, "asks": _}:
                    self.order_book = parse_order_book(order_book)
                    self.order_book["quotes"]["market"] = self.market

            self.order_quotes()
            pubsub.send(topic=self.topic, message=self.order_book["quotes"], silent=self.silent)
