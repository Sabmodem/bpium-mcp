from fastmcp import FastMCP
from mcp_server.tools import (
    register_catalog_tools,
    register_history_tools,
    register_record_tools,
    register_relation_tools,
    register_section_tools,
    register_system_tools
)

mcp = FastMCP("Bpium Server")
register_catalog_tools(mcp)
register_history_tools(mcp)
register_record_tools(mcp)
register_relation_tools(mcp)
register_section_tools(mcp)
register_system_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)