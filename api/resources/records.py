from typing import Any, Dict, List, Optional, Union
from api.base import BaseResource
from api.utils import check_response
import json

class RecordsResource(BaseResource):
    async def get_records(
        self,
        catalog_id: int,
        view_id: Optional[int] = None,
        fields: Optional[Union[List[Union[int, str, Dict]], str]] = None,
        search_text: Optional[str] = None,
        sort_field: Optional[int] = None,
        sort_type: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        filters: Optional[Union[List[Dict], Dict, str]] = None,
        record_ids: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список записей из каталога.
        """
        url = f"{self.api_url}/catalogs/{catalog_id}/records"
        params: Dict[str, Any] = {}

        if view_id is not None:
            params["viewId"] = view_id
        if search_text is not None:
            params["searchText"] = search_text
        if sort_field is not None:
            params["sortField"] = sort_field
        if sort_type is not None:
            params["sortType"] = sort_type
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        # Обработка фильтра по ID записей
        if record_ids:
            params["id"] = record_ids

        # Обработка параметра fields (сериализуется в JSON-строку)
        if fields is not None:
            if isinstance(fields, (list, dict)):
                params["fields"] = json.dumps(fields)
            else:
                params["fields"] = fields

        # Обработка фильтров (в формате JSON или массива)
        if filters is not None:
            if isinstance(filters, dict):
                params["filters"] = json.dumps(filters)
            else:
                # Для фильтров-массивов httpx развернет структуру через query-параметры
                params["filters"] = filters

        response = await self.client.get(url, params=params)
        check_response(response)
        result = response.json()
        return result

    async def get_record(
        self, 
        catalog_id: int, 
        record_id: int, 
        fields: Optional[List[Union[int, str]]] = None
    ) -> Dict[str, Any]:
        """Получить конкретную запись по ее ID."""
        url = f"{self.api_url}/catalogs/{catalog_id}/records/{record_id}"
        params: Dict[str, Any] = {}
        if fields:
            params["fields"] = json.dumps(fields)

        response = await self.client.get(url, params=params)
        check_response(response)
        return response.json()

    async def create_record(self, catalog_id: int, values: Dict[str, Any]) -> Dict[str, Any]:
        """Создать новую запись в каталоге."""
        url = f"{self.api_url}/catalogs/{catalog_id}/records"
        payload = {"values": values}
        
        response = await self.client.post(url, json=payload)
        check_response(response)
        return response.json()

    async def update_record(self, catalog_id: int, record_id: int, values: Dict[str, Any]) -> Dict[str, Any]:
        """Изменить существующую запись (PATCH)."""
        url = f"{self.api_url}/catalogs/{catalog_id}/records/{record_id}"
        payload = {"values": values}
        
        response = await self.client.patch(url, json=payload)
        check_response(response)
        return response.json()

    async def delete_record(self, catalog_id: int, record_id: int):
        """Удалить запись."""
        url = f"{self.api_url}/catalogs/{catalog_id}/records/{record_id}"
        
        response = await self.client.delete(url)
        check_response(response)