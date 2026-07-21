
from typing import Any, Dict, List, Optional, Union
from api.base import BaseResource
from api.utils import check_response

class RelationsResource(BaseResource):
    async def get_relations(
        self,
        catalog_id: int,
        record_id: int,
        filter_catalog_ids: Optional[List[int]] = None,
        field_id: Optional[int] = None,
        hidden_fields: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_field: Optional[int] = None,
        sort_type: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Получить список связей для конкретной записи."""
        url = f"{self.api_url}/catalogs/{catalog_id}/records/{record_id}/relations"
        params: Dict[str, Any] = {}

        if filter_catalog_ids:
            # httpx автоматически формирует повторяющиеся ключи для списков: catalogId=29&catalogId=28
            params["catalogId"] = filter_catalog_ids
        if field_id is not None:
            params["fieldId"] = field_id
        if hidden_fields is not None:
            params["hiddenFields"] = str(hidden_fields).lower()
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_field is not None:
            params["sortField"] = sort_field
        if sort_type is not None:
            params["sortType"] = sort_type

        response = await self.client.get(url, params=params)
        check_response(response)
        return response.json()