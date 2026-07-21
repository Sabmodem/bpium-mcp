from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from pydantic import Field

@tool
async def get_records(
    catalog_id: str = Field(..., description="ID каталога. Обязательный параметр.", min_length=1),
    fields: List[str] = Field(..., description="Список полей, опционально", default_factory=list),
    limit: int = Field(default=10, description="Количетсво элементов, параметр для пагинации"),
    offset: int = Field(default=0, description="Смещение от начала списка, параметр для пагинации"),
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить список записей из указанного каталога.
    Поддерживает текстовый поиск по содержимому записей.
    """
    try:
        records = await client.records.get_records(
            catalog_id=catalog_id,
            fields=fields,
            limit=limit,
            offset=offset
        )
        return json.dumps(records, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def get_record(
    catalog_id: str = Field(..., description="ID каталога. Обязательный параметр.", min_length=1),
    record_id: Optional[int] = Field(..., description="ID записи, опционально"),
    fields: List[str] = Field(..., description="Список полей, опционально", default_factory=list),
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить одну конкретную запись по ее ID.
    """
    try:
        record = await client.records.get_record(
            catalog_id=catalog_id,
            record_id=record_id, 
            fields=fields
        )
        return json.dumps(record, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_record_tools(mcp: FastMCP):
    mcp.add_tool(get_records)
    mcp.add_tool(get_record)
