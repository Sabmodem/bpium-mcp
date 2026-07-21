import json
from typing import Any, Dict, List, Optional
from api.base import BaseResource
from api.utils import check_response

class CatalogsResource(BaseResource):
    async def get_catalogs(self, section_id: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{self.api_url}/catalogs"
        params = {}
        if section_id:
            params["sectionId"] = section_id
            
        response = await self.client.get(url, params=params)
        check_response(response)
        return response.json()

    async def get_catalog(self, catalog_id: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        url = f"{self.api_url}/catalogs/{catalog_id}"
        params = {}
        if fields:
            params["fields"] = json.dumps(fields)
            
        response = await self.client.get(url, params=params)
        check_response(response)
        return response.json()

    async def create_catalog(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_url}/catalogs"
        response = await self.client.post(url, json=schema)
        check_response(response)
        return response.json()

    async def update_catalog(self, catalog_id: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_url}/catalogs/{catalog_id}"
        response = await self.client.patch(url, json=schema)
        check_response(response)
        return response.json()

    async def delete_catalog(self, catalog_id: str) -> Dict[str, Any]:
        url = f"{self.api_url}/catalogs/{catalog_id}"
        response = await self.client.delete(url)
        check_response(response)
        return response.json()