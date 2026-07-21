import json
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from fastmcp.tools import tool
from fastmcp.dependencies import Depends

from mcp_server.utils import sanitize_catalog_fields, sanitize_catalogs_list
from mcp_server.dependencies import get_bpium_client
from api.client import BpiumClient, BpiumClientException
from pydantic import Field

@tool
async def get_catalogs(
    section_id: str = Field(..., description="ID секции. Обязательный параметр.", min_length=1),
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить компактный список доступных каталогов Bpium (ID и названия).
    Можно отфильтровать по section_id.
    """
    try:
        raw_catalogs = await client.catalogs.get_catalogs(section_id=section_id)
        clean_catalogs = sanitize_catalogs_list(raw_catalogs)
        return json.dumps(clean_catalogs, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

@tool
async def get_catalog(
    catalog_id: str = Field(..., description="ID каталога. Обязательный параметр.", min_length=1),
    fields: List[str] = Field(..., description="Список полей. Опционально", default_factory=list),
    client: BpiumClient = Depends(get_bpium_client)    
) -> str:
    """
    Получить структуру полей каталога (ID полей, их названия и типы).
    ОБЯЗАТЕЛЬНО вызывайте перед созданием или обновлением записей, 
    чтобы узнать, какие ID полей использовать в 'values'.
    """
    try:
        raw_schema = await client.catalogs.get_catalog(
            catalog_id=catalog_id, 
            fields=fields
        )
        return json.dumps(sanitize_catalog_fields(raw_schema), ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_catalog_tools(mcp: FastMCP):
    mcp.add_tool(get_catalogs)
    mcp.add_tool(get_catalog)
