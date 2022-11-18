import time
import asyncio
import numpy as np
from typing import Any


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


class Rate_Limit_Manager:
    def __init__(self, n: int, T: int):
        self.n = n
        self.T = T

        self.d: dict[str, Rate_limit] = {}

    def __getitem__(self, ticker: str) -> Rate_limit:
        if ticker not in self.d.keys():
            self.d[ticker] = Rate_limit(n=self.n, T=self.T)

        return self.d[ticker]


rate_limits: dict[str, Any] = {
    "get": Rate_limit(n=95, T=10),
    "cancel_one": Rate_limit(n=250, T=10),
    "cancel_all": Rate_limit(n=3, T=10),
    "limit_orders": Rate_Limit_Manager(n=4, T=10),
    "market_orders": Rate_Limit_Manager(n=10, T=10),
}
