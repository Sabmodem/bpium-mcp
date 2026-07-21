from typing import Any, Dict, List, Optional, Union
from api.base import BaseResource
from api.utils import check_response

class SectionsResource(BaseResource):
    async def get_sections(self) -> List[Dict[str, Any]]:
        url = f"{self.api_url}/sections"
        response = await self.client.get(url)
        check_response(response)
        return response.json()

    async def get_section(self, section_id: Union[int, str]) -> Dict[str, Any]:
        url = f"{self.api_url}/sections/{section_id}"
        response = await self.client.get(url)
        check_response(response)
        return response.json()

    async def create_section(self, name: str, icon: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.api_url}/sections"
        payload: Dict[str, Any] = {"name": name}
        if icon:
            payload["icon"] = icon

        response = await self.client.post(url, json=payload)
        check_response(response)
        return response.json()

    async def update_section(self, section_id: Union[int, str], schema: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_url}/sections/{section_id}"
        response = await self.client.patch(url, json=schema)
        check_response(response)
        return response.json()

    async def delete_section(self, section_id: Union[int, str]) -> Dict[str, Any]:
        url = f"{self.api_url}/sections/{section_id}"
        response = await self.client.delete(url)
        check_response(response)
        return response.json()