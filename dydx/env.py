import os
from dotenv import load_dotenv


load_dotenv()

# Account
ACCOUNT_ID = int(os.environ.get("ACCOUNT_ID", 0))
ETH_ADDRESS = os.environ.get("ETH_ADDRESS", "")
ETH_PRIVATE_KEY = os.environ.get("ETH_PRIVATE_KEY", "")
STARK_PRIVATE_KEY = os.environ.get("STARK_PRIVATE_KEY", "")

DYDX_API_KEY = {
    "key": os.environ.get("DYDX_KEY", ""),
    "secret": os.environ.get("DYDX_SECRET", ""),
    "passphrase": os.environ.get("DYDX_PASSPHRASE", ""),
}
