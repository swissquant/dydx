from link import pubsub

from .client import WS

from dydx.rest import fetch_account
from dydx.parser import parse_order, parse_position, parse_fill
from dydx.client import client_priv, generate_timestamp, sign


class WS_Account(WS):
    topic_fills = "dydx:fills"
    topic_orders = "dydx:orders"
    topic_positions = "dydx:positions"

    def __init__(self):
        self.order_summary: dict[str, dict] = {}

    async def subscribe(self):
        """
        Subscribe to the account channel
        """
        # Fetching the account informations
        account = await fetch_account()

        # Generating the signature
        timestamp = generate_timestamp()
        signature = sign(
            request_path="/ws/accounts",
            method="GET",
            timestamp=timestamp,
        )

        # Subscribing
        await super().subscribe(
            channel="v3_accounts",
            accountNumber=account["account_number"],
            apiKey=client_priv.private.api_key_credentials["key"],
            signature=signature,
            timestamp=timestamp,
            passphrase=client_priv.private.api_key_credentials["passphrase"],
        )

    def process_fills(self, fills: list):
        for _fill in fills:
            # Parsing the fill
            fill = parse_fill(_fill)

            # Creating the order summary if it doesn't exist
            order_id = fill.get("order_id", "")
            if order_id not in self.order_summary.keys():
                self.order_summary[order_id] = {"size": 0, "price_times_size": 0, "fees": 0}

            # Updating the order summary
            self.order_summary[order_id]["size"] += fill.get("size", 0)
            self.order_summary[order_id]["price_times_size"] += fill.get("size", 0) * fill.get("price", 0)
            self.order_summary[order_id]["fees"] += fill.get("fee", 0)

            # Broadcasting
            pubsub.send(topic=self.topic_fills, message=fill)

    def process_positions(self, positions: list):
        for position in positions:
            pubsub.send(topic=self.topic_positions, message=parse_position(position))

    def process_orders(self, orders: list):
        for _order in orders:
            # Parsing the order
            order = parse_order(_order)

            # Attaching the extra informations from the fills
            if order.get("id", "") in self.order_summary.keys():
                order_summary = self.order_summary[order.get("id", "")]

                # Calculating the average price
                if order_summary["size"] != 0:
                    order["price_average"] = order_summary["price_times_size"] / order_summary["size"]
                else:
                    order["price_average"] = None

                # Calculating the fees
                order["fees"] = order_summary["fees"]
            else:
                order["price_average"] = None
                order["fees"] = 0

            # Broadcasting
            pubsub.send(topic=self.topic_orders, message=order)

    async def start(self):
        # Connecting and subscribing to the WS
        await self.connect()
        await self.subscribe()

        while True:
            # Waiting for a new message
            msg = await self.receive()

            # Processing the message
            self.process_fills(fills=msg.get("fills", []))
            self.process_orders(orders=msg.get("orders", []))
            self.process_positions(positions=msg.get("positions", []))
