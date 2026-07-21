import pytest
import httpx
from api.client import BpiumClient
from api.exceptions import BpiumClientException

@pytest.fixture
async def client():
    async with BpiumClient(base_url="https://test.bpium.ru") as c:
        yield c

@pytest.mark.asyncio
class TestBpiumClientLifecycle:
    async def test_context_manager_closes_client(self):
        """Проверка закрытия сессии при выходе из контекстного менеджера."""
        async with BpiumClient(base_url="https://test.bpium.ru") as c:
            assert c._is_closed is False
        assert c._is_closed is True

@pytest.mark.asyncio
class TestRecordsResource:
    async def test_get_records_query_params_serialization(self, client, mocker):
        """Проверка корректной сериализации сложных query-параметров (fields, filters)."""
        mock_response = httpx.Response(status_code=200, json=[])
        mock_get = mocker.patch.object(client.client, "get", return_value=mock_response)

        fields = ["id", "title"]
        filters = {"1": "val"}
        
        await client.records.get_records(
            catalog_id=10, 
            limit=20, 
            offset=5, 
            fields=fields, 
            filters=filters
        )

        # Проверяем, с какими params был вызван httpx
        assert mock_get.called
        call_params = mock_get.call_args.kwargs["params"]
        assert call_params["limit"] == 20
        assert call_params["offset"] == 5
        assert call_params["fields"] == '["id", "title"]'
        assert call_params["filters"] == '{"1": "val"}'

    async def test_update_record_patch_payload(self, client, mocker):
        """Проверка формирования payload при обновлении записи через PATCH."""
        mock_response = httpx.Response(status_code=200, json={"id": 1, "values": {"1": "updated"}})
        mock_patch = mocker.patch.object(client.client, "patch", return_value=mock_response)

        res = await client.records.update_record(catalog_id=10, record_id=1, values={"1": "updated"})

        assert res["values"]["1"] == "updated"
        mock_patch.assert_called_once_with(
            "/api/v1/catalogs/10/records/1",
            json={"values": {"1": "updated"}}
        )

    async def test_delete_record_success(self, client, mocker):
        """Проверка вызова метода DELETE."""
        mock_response = httpx.Response(status_code=200, json={})
        mock_delete = mocker.patch.object(client.client, "delete", return_value=mock_response)

        await client.records.delete_record(catalog_id=10, record_id=1)
        mock_delete.assert_called_once_with("/api/v1/catalogs/10/records/1")