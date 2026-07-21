from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient, BpiumClientException
from mcp_server.dependencies import get_bpium_client
import json
from typing import Union, Optional, Dict, Any
from fastmcp import FastMCP
from pydantic import Field

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
    section_id: str = Field(..., description="ID секции. Обязательный параметр.", min_length=1),
    client: BpiumClient = Depends(get_bpium_client)
) -> str:
    """
    Получить детальную информацию о конкретном разделе по его ID.
    """
    try:
        section = await client.sections.get_section(section_id=section_id)
        return json.dumps(section, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

def register_section_tools(mcp: FastMCP):
    mcp.add_tool(get_section)
    mcp.add_tool(get_sections)