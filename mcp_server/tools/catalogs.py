from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from async_lru import alru_cache
from mcp_server.utils import sanitize_catalog_fields, sanitize_catalogs_list
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Optional, Dict, Any
from fastmcp import FastMCP


# Чистая функция для получения данных (без кэширования)
async def _fetch_catalog_schema(
    catalog_id: str,
    client: BpiumClient
) -> Dict[str, Any]:
    raw_schema = await client.catalogs.get_catalog(catalog_id=catalog_id)
    return sanitize_catalog_fields(raw_schema)


# Кэшируемая функция без Depends
@alru_cache(maxsize=100)
async def _get_cached_catalog_schema(
    catalog_id: str,
    client: BpiumClient
) -> Dict[str, Any]:
    return await _fetch_catalog_schema(catalog_id, client)


@tool
async def get_catalogs(
    section_id: Optional[str] = None,
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
async def create_catalog(
    schema: Dict[str, Any],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Создать новый каталог в Bpium.
    
    :param schema: Словарь со схемой каталога (например, title, sectionId, fields и т.д.).
    """
    try:
        new_catalog = await client.catalogs.create_catalog(schema=schema)
        _get_cached_catalog_schema.cache_clear()
        return json.dumps(new_catalog, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def update_catalog(
    catalog_id: str, 
    schema: Dict[str, Any],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Изменить существующий каталог (PATCH). Позволяет менять название, добавлять или редактировать поля.
    
    :param catalog_id: ID редактируемого каталога.
    :param schema: Словарь с изменяемыми атрибутами каталога.
    """
    try:
        updated_catalog = await client.catalogs.update_catalog(catalog_id=catalog_id, schema=schema)
        # Сбрасываем кэш схемы для этого каталога
        _get_cached_catalog_schema.cache_clear()
        return json.dumps(updated_catalog, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def delete_catalog(
    catalog_id: str,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Удалить каталог по его ID.
    """
    if not catalog_id:
        raise ValueError("ID каталога является обязательным") 
    try:
        await client.catalogs.delete_catalog(catalog_id=catalog_id)
        _get_cached_catalog_schema.cache_clear()
        return f"Каталог {catalog_id} успешно удален."
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def get_catalog_schema(
    catalog_id: str,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить структуру полей каталога (ID полей, их названия и типы).
    ОБЯЗАТЕЛЬНО вызывайте перед созданием или обновлением записей, 
    чтобы узнать, какие ID полей использовать в 'values'.
    """
    try:
        schema = await _get_cached_catalog_schema(catalog_id, client)
        return json.dumps(schema, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_catalog_tools(mcp: FastMCP):
    mcp.add_tool(get_catalogs)
    mcp.add_tool(get_catalog_schema)
    mcp.add_tool(create_catalog)
    mcp.add_tool(update_catalog)
    mcp.add_tool(delete_catalog)