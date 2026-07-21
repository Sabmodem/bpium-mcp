from typing import Any, Dict, List, Optional, Union
from api.base import BaseResource
from api.utils import check_response

class SystemResource(BaseResource):
    async def get_me(self):
        url = f"{self.api_url}/profile/me"
        params = {}
        response = await self.client.get(url, params=params)
        check_response(response)
        result = response.json()
        return result
