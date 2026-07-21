import pytest
import json
from unittest.mock import AsyncMock
from mcp_server.tools.records import get_records, get_record
from api.exceptions import BpiumClientException

@pytest.mark.asyncio
class TestMCPRecordTools:
    async def test_get_records_tool_success(self, mocker):
        """MCP Tool возвращает JSON-строку при успешном ответе от API."""
        mock_client = AsyncMock()
        mock_client.records.get_records.return_value = [{"id": 1, "values": {}}]

        result_str = await get_records(
            catalog_id="10",
            fields=[],
            limit=10,
            offset=0,
            client=mock_client
        )

        parsed = json.loads(result_str)
        assert isinstance(parsed, list)
        assert parsed[0]["id"] == 1

    async def test_get_record_tool_handles_bpium_exception(self, mocker):
        """MCP Tool перехватывает BpiumClientException и возвращает понятную строку об ошибке."""
        mock_client = AsyncMock()
        mock_client.records.get_record.side_effect = BpiumClientException(404, "Ресурс не найден")

        result_str = await get_record(
            catalog_id="10",
            record_id=999,
            fields=[],
            client=mock_client
        )

        assert "Ошибка Bpium API" in result_str
        assert "404" in result_str