from link import pubsub

from .client import WS

from dydx.rest import fetch_account
from dydx.parser import parse_order, parse_position
from dydx.client import client_priv, generate_timestamp, sign


class WS_Account(WS):
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
        if len(fills) > 0:
            # TODO
            pass

    def process_positions(self, positions: list):
        for position in positions:
            pubsub.send(topic="dydx:positions", message=parse_position(position))

    def process_orders(self, orders: list):
        for order in orders:
            pubsub.send(topic="dydx:orders", message=parse_order(order))

    async def start(self):
        # Connecting and subscribing to the WS
        await self.connect()
        await self.subscribe()

        while True:
            # Waiting for a new message
            msg = await self.receive()

            # Processing the message
            self.process_fills(fills=msg.get("fills", []))
            self.process_positions(positions=msg.get("positions", []))
            self.process_orders(orders=msg.get("orders", []))
