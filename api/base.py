import httpx
from api.exceptions import BpiumClientException

class BaseResource:
    def __init__(
        self, 
        client: httpx.AsyncClient,
        api_url: str
    ):
        self.client = client
        self.api_url = api_url
