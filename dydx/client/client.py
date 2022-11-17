import aiohttp
from urllib.parse import urlencode

from .rate_limit import rate_limits
from .client_priv import client_priv, generate_timestamp, sign


class Client_Async:
    def __init__(self, url: str = "https://api.dydx.exchange", rate_limit: float = 0.1):
        self.url = url
        self.rate_limit = rate_limit

        self.next_call = 0
        self.session = None
        self.markets = None

    async def get_session(self):
        """
        Get the session. Create one if not yet created
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

    def construct_url(self, endpoint: str, **kwargs):
        """
        Construct the url
        """
        return f"{self.url}/{endpoint}?{urlencode(kwargs)}"

    def authenticate(self, endpoint: str, method: str = "GET", data={}):
        """
        Return the authentication headers
        """
        timestamp = generate_timestamp()
        headers = {
            "DYDX-SIGNATURE": sign(
                request_path="/" + endpoint,
                method=method,
                timestamp=timestamp,
                data=data,
            ),
            "DYDX-API-KEY": client_priv.api_key_credentials["key"],
            "DYDX-TIMESTAMP": timestamp,
            "DYDX-PASSPHRASE": client_priv.api_key_credentials["passphrase"],
            "DYDX-ACCOUNT-NUMBER": "0",
        }

        return headers

    async def get(self, endpoint: str, container: str = "", **kwargs):
        """
        Get the data for the given endpoint and parameters
        """
        await self.get_session()
        await rate_limits["get"].throttle()

        # Constructing the URL
        url = self.construct_url(endpoint=endpoint, **kwargs)

        # Constructing the headers
        if len(kwargs) > 0:
            headers = self.authenticate(endpoint=f"{endpoint}?{urlencode(kwargs)}")
        else:
            headers = self.authenticate(endpoint=endpoint)

        # Fetching the URL content
        async with self.session.get(url=url, headers=headers) as resp:  # type: ignore
            result = await resp.json()

        if resp.status != 200:
            raise Exception(f"Request failed: {resp.status} - {result['errors']}")

        return result.get(container, result)

    async def post(self, endpoint: str, container: str = "", **kwargs):
        """
        Post the data to the given endpoint
        """
        await self.get_session()

        # Constructing the URL
        url = self.construct_url(endpoint=endpoint)

        # Constructing the headers
        headers = self.authenticate(endpoint=endpoint, method="POST", data=kwargs)

        # Fetching the URL content
        async with self.session.post(url=url, headers=headers, json=kwargs) as resp:  # type: ignore
            result = await resp.json()

        if resp.status != 201:
            raise Exception(f"Request failed: {resp.status} - {result['errors']}")

        return result[container]

    async def delete(self, endpoint: str, container: str = "", **kwargs):
        """
        Post the data to the given endpoint
        """
        await self.get_session()

        # Constructing the URL
        url = self.construct_url(endpoint=endpoint, **kwargs)

        # Constructing the headers
        headers = self.authenticate(endpoint=endpoint, method="DELETE", data=kwargs)

        # Fetching the URL content
        async with self.session.delete(url=url, headers=headers) as resp:  # type: ignore
            result = await resp.json()

        if resp.status != 200:
            raise Exception(f"Request failed: {resp.status} - {result['errors']}")

        return result[container]


client = Client_Async()
