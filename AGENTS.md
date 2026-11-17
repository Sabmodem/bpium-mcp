# Bpium MCP Server - Agent Instructions

## Project Overview
FastMCP server exposing Bpium CRM API as tools. Uses `uv` for dependency management, `pytest-asyncio` for testing, and Docker for deployment.

## Developer Commands

### Setup & Dependencies
```bash
uv sync              # Install dependencies
uv run main.py       # Run dev server locally
```

### Testing
```bash
uv run pytest tests/ -v
uv run pytest tests/<file>.py -v  # Single test file
```

### Docker
```bash
# Build & run
docker-compose up --build

# Or build image directly
docker build -t bpium-mcp .
```

## Architecture

### Entry Point
- `main.py` - FastMCP server bootstrap
- `mcp_server/tools/` - Tool registration modules (catalogs, records, sections, system)
- `api/` - Bpium REST client layer
- `api/client.py` - `BpiumClient` with context manager lifecycle

### tool flow
1. MCP tool call → `mcp_server/tools/<resource>.py`
2 Tool → `get_bpium_client()` (from `dependencies.py`) → `BpiumClient.login_post()`
3. Tool → `api/resources/<resource>.py` → httpx calls → `check_response()` error handling

### Environment
- Required env vars: `URL`, `LOGIN`, `PASSWORD` (see `.env_example`)
- Default URL: `https://sd-demo.bpium.ru`

## Testing Notes
- All tests async; `pytest` configured with `asyncio_mode = "auto"`
- `BpiumClient` tested via `httpx` mock ` AsyncMock` for tools
- `check_response()` maps HTTP codes to `BpiumClientException` (400/401/403/404/429/500)

## Gotchas
- tools return JSON strings (MCP requirement), parsed by caller
- `BpiumClient` uses POST `/ auth/login` for session cookie auth
- fields/filters params serialized as JSON strings in query params
