import datetime

from dydx3 import Client

from dydx.env import ETH_PRIVATE_KEY


# Generating the client priv to do the signature later on
client_priv = Client(
    host="https://api.dydx.exchange",
    eth_private_key=ETH_PRIVATE_KEY,
)
client_priv.stark_private_key = client_priv.onboarding.derive_stark_key()


def generate_timestamp() -> str:
    """
    Generate the timestamp in the needed format for the signature
    """
    timestamp = (
        datetime.datetime.utcnow().strftime(
            "%Y-%m-%dT%H:%M:%S.%f",
        )[:-3]
        + "Z"
    )

    return timestamp


def sign(request_path: str, method: str, timestamp: str, data: dict = {}) -> str:
    """
    Sign the given request
    """
    signature = client_priv.private.sign(
        request_path=request_path,
        method=method,
        iso_timestamp=timestamp,
        data=data,
    )

    return signature
