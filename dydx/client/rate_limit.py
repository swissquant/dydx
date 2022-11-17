import time
import asyncio
import numpy as np


class Rate_limit:
    def __init__(self, n: int = 0, T: float = 0):
        self.n = n
        self.T = T
        self.timestamps: list[float] = []

    async def throttle(self):
        """
        Throttle the call if there is a need to rate limit in order to avoid DDoSing the distant server
        """
        self.timestamps.append(time.time())
        self.timestamps = self.timestamps[-self.n :]

        if len(self.timestamps) == self.n:
            sleep = np.mean(self.timestamps) + self.T - time.time()
            await asyncio.sleep(sleep)


rate_limits: dict[str, Rate_limit] = {
    "get": Rate_limit(n=95, T=10),
    "cancel_one": Rate_limit(n=250, T=10),
    "cancel_all": Rate_limit(n=3, T=10),
}
