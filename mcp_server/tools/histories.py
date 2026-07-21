from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Optional
from fastmcp import FastMCP

@tool
async def get_histories(
    catalog_id: int,
    record_id: Optional[int] = None,
    user_id: Optional[int] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = None,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить историю изменений записей в каталоге.
    Позволяет узнать, кто, когда и что изменил.
    
    :param catalog_id: ID каталога.
    :param record_id: ID конкретной записи (опционально, чтобы получить историю только по ней).
    :param user_id: Фильтр по ID пользователя, совершившего изменения.
    :param limit: Лимит выводимых записей истории.
    :param offset: Смещение для пагинации.
    """
    try:
        histories = await client.histories.et_histories(
            catalog_id=catalog_id,
            record_id=record_id,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        return json.dumps(histories, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"


def register_history_tools(mcp: FastMCP):
    mcp.add_tool(get_histories)