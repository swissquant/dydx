import asyncio

from loguru import logger


class Executor:
    def __init__(
        self,
        max_tentatives=10,
        cooldown=0.1,
    ):
        self.max_tentatives = max_tentatives
        self.cooldown = cooldown

    async def submit(self, coroutine, **kwargs):
        for i in range(0, self.max_tentatives):
            try:
                # Executing the api call and breaking the loop
                # if the earlier is successful
                result = await coroutine(**kwargs)
                return result
            except Exception:
                await asyncio.sleep(self.cooldown)

            logger.info(f"Request failed ({i+1} tentatives)")

        raise Exception("Failed")
