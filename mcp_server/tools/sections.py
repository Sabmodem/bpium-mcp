from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Union, Optional, Dict, Any
from fastmcp import FastMCP

@tool
async def get_sections(client: BpiumClient = Depends(get_bpium_client)) -> str:
    """
    Получить список всех разделов (отделов) Bpium.
    Разделы используются для логической группировки каталогов.
    """
    try:
        sections = await client.sections.get_sections()
        return json.dumps(sections, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

@tool
async def get_section(
    section_id: Union[int, str],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить детальную информацию о конкретном разделе по его ID.
    """
    try:
        section = await client.get_section(section_id=section_id)
        return json.dumps(section, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

@tool
async def create_section(
    name: str, 
    icon: Optional[str] = None,
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Создать новый раздел для каталогов.
    
    :param name: Название создаваемого раздела.
    :param icon: Название иконки раздела (опционально, например 'icon1').
    """
    try:
        new_section = await client.create_section(name=name, icon=icon)
        return json.dumps(new_section, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

@tool
async def update_section(
    section_id: Union[int, str], 
    schema: Dict[str, Any],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Изменить настройки или содержимое раздела (PATCH).
    
    :param section_id: ID редактируемого раздела.
    :param schema: Словарь с изменяемыми параметрами. 
                  Пример: {"name": "Новое имя", "catalogsPriorities": ["5", "3", "7"]}
    """
    try:
        updated_section = await client.update_section(section_id=section_id, schema=schema)
        return json.dumps(updated_section, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

@tool
async def delete_section(
    section_id: Union[int, str],
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Удалить раздел по его ID.
    """
    try:
        await client.sections.delete_section(section_id=section_id)
        return f"Раздел {section_id} успешно удален."
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

def register_section_tools(mcp: FastMCP):
    mcp.add_tool(get_section)
    mcp.add_tool(get_sections)
    mcp.add_tool(create_section)
    mcp.add_tool(update_section)
    mcp.add_tool(delete_section)    