import json
import websockets

from loguru import logger


class WS:
    url = "wss://api.dydx.exchange/v3/ws"

    async def connect(self):
        self.ws = await websockets.connect(self.url)  # type: ignore

    async def subscribe(self, channel: str, **args):
        """
        Subsribe to a channel
        """
        # Subscribing to the desired topic
        request = {
            "type": "subscribe",
            "channel": channel,
        }
        request.update(args)
        await self.ws.send(json.dumps(request))
        logger.info(f"Subscribed to {channel}")

    async def receive(self) -> dict:
        while True:
            # Waiting for a message
            msg = await self.ws.recv()
            msg = json.loads(msg)

            # Returning the message only if there is contents
            try:
                return msg["contents"]
            except Exception:
                pass
