from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Optional, Dict, Any
from fastmcp import FastMCP

@tool
async def get_records(
    catalog_id: int,
    search_text: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = None,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить список записей из указанного каталога.
    Поддерживает текстовый поиск по содержимому записей.
    """
    try:
        records = await client.records.get_records(
            catalog_id=catalog_id,
            search_text=search_text,
            limit=limit,
            offset=offset
        )
        return json.dumps(records, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def get_record(
    catalog_id: int, 
    record_id: int,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить одну конкретную запись по ее ID.
    """
    try:
        record = await client.records.get_record(catalog_id=catalog_id, record_id=record_id)
        return json.dumps(record, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def create_record(
    catalog_id: int, 
    values: Dict[str, Any],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Создать новую запись в каталоге.
    
    :param catalog_id: ID каталога.
    :param values: Словарь со значениями полей вида {"1": "Текст", "2": 100}, 
                   где ключи — это ID полей (из get_catalog_schema).
    """
    try:
        new_record = await client.records.create_record(catalog_id=catalog_id, values=values)
        return json.dumps(new_record, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def update_record(
    catalog_id: int, 
    record_id: int, 
    values: Dict[str, Any],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Изменить (PATCH) существующую запись по её ID.
    
    :param catalog_id: ID каталога.
    :param record_id: ID редактируемой записи.
    :param values: Словарь с обновляемыми полями вида {"1": "Новый текст"}.
    """
    try:
        updated_record = await client.records.update_record(
            catalog_id=catalog_id, 
            record_id=record_id, 
            values=values
        )
        return json.dumps(updated_record, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


@tool
async def delete_record(
    catalog_id: int, 
    record_id: int,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Удалить запись из каталога.
    """
    try:
        await client.records.delete_record(catalog_id=catalog_id, record_id=record_id)
        return f"Запись {record_id} из каталога {catalog_id} успешно удалена."
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_record_tools(mcp: FastMCP):
    mcp.add_tool(get_records)
    mcp.add_tool(get_record)
    mcp.add_tool(create_record)
    mcp.add_tool(update_record)
    mcp.add_tool(delete_record)