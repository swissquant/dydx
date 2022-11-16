import os
from dotenv import load_dotenv


load_dotenv()

# Account
ACCOUNT_ID = int(os.environ.get("ACCOUNT_ID", 0))
ETH_PRIVATE_KEY = os.environ.get("ETH_PRIVATE_KEY", "")
