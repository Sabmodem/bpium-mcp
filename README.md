# Bpium MCP Server

FastMCP server that exposes Bpium CRM API as MCP tools.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

1. Copy `.env_example` to `.env` and configure:
   ```bash
   cp .env_example .env
   ```

2. Set environment variables in `.env`:
   ```
   URL=https://your-domain.bpium.ru
   LOGIN=youremail@domain.ru
   PASSWORD=yourpassword
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

## Running

### Local Development
```bash
uv run main.py
```

### Docker
```bash
docker-compose up --build
```

## API Endpoints

The server exposes an SSE endpoint at `http://localhost:8000`.

## Tools

- **catalogs** - Manage BPM catalogs
- **records** - CRUD operations for records
- **sections** - Section management
- **system** - System information

## Testing

```bash
uv run pytest tests/ -v
```

## Architecture

```
main.py              # FastMCP bootstrap
├── mcp_server/
│   ├── tools/       # Tool registrations
│   └── dependencies.py  # Client lifecycle
└── api/
    ├── client.py    # BpiumClient with HTTP session
    ├── resources/   # API resource clients
    └── utils.py     # Response handling & error mapping
```
