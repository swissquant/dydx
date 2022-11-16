import json
import websockets

from loguru import logger


class WS:
    url = "wss://api.dydx.exchange/v3/ws"

    async def subscribe(self, channel: str, **args):
        """
        Subsribe to a channel
        """
        # Connecting to the websocket
        self.ws = await websockets.connect(self.url)  # type: ignore

        # Subscribing to the desired topic
        request = {
            "type": "subscribe",
            "channel": channel,
        }.update(args)
        await self.ws.send(json.dumps(request))
        logger.info(f"Subscribed to {channel} - {args.get('id', '')}")

    async def receive(self):
        while True:
            # Waiting for a message
            msg = await self.ws.recv()
            msg = json.loads(msg)

            # Returning the message only if there is contents
            try:
                return msg["contents"]
            except Exception:
                pass
