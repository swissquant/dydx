import datetime
from loguru import logger
from decimal import Decimal
from functools import wraps


def restart_on_failure(func):
    """
    Restart the function on failure
    """

    @wraps(func)
    async def run(*args):
        while True:
            try:
                await func(*args)
            except Exception as e:
                logger.error(e)

    return run


def datetime_to_iso(dt: datetime.datetime) -> str:
    """
    Transform a datetime object to an ISO string
    """
    return (
        dt.strftime(
            "%Y-%m-%dT%H:%M:%S.%f",
        )[:-3]
        + "Z"
    )


def timestamp_to_iso(timestamp: float) -> str:
    """
    Transform a timestamp to an ISO string
    """
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return datetime_to_iso(dt=dt)


def round_by(x: float, base: float):
    """
    Round the number x by increment of base
    """
    x_rounded = Decimal(str(base)) * round(Decimal(str(x)) / Decimal(str(base)))

    return float(x_rounded)
