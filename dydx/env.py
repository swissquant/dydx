import os
from dotenv import load_dotenv


load_dotenv()

# Account
DYDX_ETH_ADDRESS = os.environ.get("DYDX_ETH_ADDRESS", "")
DYDX_STARK_PRIVATE_KEY = os.environ.get("DYDX_STARK_PRIVATE_KEY", "")

DYDX_API_CREDENTIALS = {
    "key": os.environ.get("DYDX_API_KEY", ""),
    "secret": os.environ.get("DYDX_API_SECRET", ""),
    "passphrase": os.environ.get("DYDX_API_PASSPHRASE", ""),
}
