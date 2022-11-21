import datetime

from dydx3 import Client
from dydx3.starkex.helpers import private_key_to_public_key_pair_hex

from dydx.env import DYDX_ETH_ADDRESS, DYDX_STARK_PRIVATE_KEY, DYDX_API_CREDENTIALS


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


def derive_stark_key_from_private_key(stark_private_key):
    public_x, public_y = private_key_to_public_key_pair_hex(stark_private_key)
    return {"public_key": public_x, "public_key_y_coordinate": public_y, "private_key": stark_private_key}


# Generating the private client to sign private requests to DYDX
client_priv = Client(
    host="https://api.dydx.exchange",
    default_ethereum_address=DYDX_ETH_ADDRESS,
    api_key_credentials=DYDX_API_CREDENTIALS,
)
client_priv.stark_private_key = derive_stark_key_from_private_key(DYDX_STARK_PRIVATE_KEY)
