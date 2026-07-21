from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Optional, List
from fastmcp import FastMCP

@tool
async def get_record_relations(
    catalog_id: int,
    record_id: int,
    filter_catalog_ids: Optional[List[int]] = None,
    field_id: Optional[int] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = None,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить список связанных записей для конкретной записи.
    
    :param catalog_id: ID исходного каталога.
    :param record_id: ID записи, для которой ищем связи.
    :param filter_catalog_ids: Фильтр по ID связанных каталогов (покажет связи только с ними).
    :param field_id: Фильтр по конкретному полю связи (field_id).
    :param limit: Лимит количества результатов.
    :param offset: Смещение для пагинации.
    """
    try:
        relations = await client.relations.get_relations(
            catalog_id=catalog_id,
            record_id=record_id,
            filter_catalog_ids=filter_catalog_ids,
            field_id=field_id,
            limit=limit,
            offset=offset
        )
        return json.dumps(relations, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_relation_tools(mcp: FastMCP):
    mcp.add_tool(get_record_relations)