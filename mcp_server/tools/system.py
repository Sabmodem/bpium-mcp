from fastmcp.tools import tool
from fastmcp.dependencies import Depends
from api.client import BpiumClient
from mcp_server.dependencies import get_bpium_client
from fastmcp import FastMCP
import json

@tool()
async def get_me(client: BpiumClient = Depends(get_bpium_client)) -> str:
    """
    Получить информацию о текущем авторизованном пользователе/профиле.
    """
    try:
        me_info = await client.system.get_me()
        return json.dumps(me_info, ensure_ascii=False)
    except BpiumClientException as e:
        return f"Ошибка Bpium API: {e}"

def register_system_tools(mcp: FastMCP):
    mcp.add_tool(get_me)