import json
from typing import Any, Dict, List, Optional
from api.base import BaseResource
from api.utils import check_response

class HistoriesResource(BaseResource):
    async def get_histories(
        self, 
        catalog_id: int, 
        record_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_type: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Получить историю изменений записей."""
        url = f"{self.api_url}/histories"
        params: Dict[str, Any] = {"catalogId": catalog_id}
        
        if record_id is not None:
            params["recordId"] = record_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["from"] = offset  # По документу: from аналогично offset
        if sort_type is not None:
            params["sortType"] = sort_type
        if user_id is not None:
            params["userId"] = user_id

        response = await self.client.get(url, params=params)
        check_response(response)
        return response.json()