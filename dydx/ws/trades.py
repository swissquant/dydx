from link import pubsub

from .client import WS


def parse_trade(trade):
    match trade:
        case {"side": str(side), "size": size, "price": price}:
            trade = {
                "side": side.lower(),
                "size": float(size),
                "price": float(price),
            }

            return trade


class WS_Trades(WS):
    def __init__(self, market: str, silent: bool = True):
        self.market = market
        self.silent = silent

    def parse(self, trades):
        """
        Parse the raw trade data
        """
        for trade in trades:
            trade["size"] = float(trade["size"])
            trade["price"] = float(trade["price"])

        return trades

    async def start(self):
        # Subscribing to the trades channel
        await self.connect()
        await self.subscribe(channel="v3_trades", id=self.market)

        while True:
            # Waiting for a new message
            trades = (await self.receive()).get("trades", [])

            # Parsing the trades
            for trade in trades:
                pubsub.send(topic="dydx:trades", message=parse_trade(trade), silent=self.silent)
