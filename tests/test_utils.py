import pytest
import httpx
from api.utils import check_response
from api.exceptions import BpiumClientException
from mcp_server.utils import sanitize_catalog_fields, sanitize_catalogs_list

class TestCheckResponse:
    def test_check_response_success_status_codes(self):
        """Проверка всех успешных статус-кодов (200, 201, 204)."""
        for code in [200, 201, 204]:
            response = httpx.Response(status_code=code, json={"ok": True})
            check_response(response)  # Не должно выбрасывать исключений

    @pytest.mark.parametrize("status_code,expected_msg", [
        (400, "Некорректный запрос"),
        (401, "Ошибка авторизации"),
        (403, "Доступ запрещён"),
        (404, "Ресурс не найден"),
        (429, "Превышен лимит запросов"),
        (500, "Внутренняя ошибка сервера"),
    ])
    def test_check_response_known_errors(self, status_code, expected_msg):
        """Проверка маппинга стандартных HTTP-ошибок в BpiumClientException."""
        response = httpx.Response(status_code=status_code, json={"error": "details"})
        
        with pytest.raises(BpiumClientException) as exc_info:
            check_response(response)
            
        assert exc_info.value.status_code == status_code
        assert expected_msg in str(exc_info.value)

    def test_check_response_handles_non_json_body(self):
        """Корректная обработка ответа с ошибкой, если тело — не JSON (например, HTML 502/504)."""
        response = httpx.Response(status_code=502, text="<html>Bad Gateway</html>")
        
        with pytest.raises(BpiumClientException) as exc_info:
            check_response(response)
            
        assert exc_info.value.status_code == 502
        assert "Тело ответа: <html>Bad Gateway</html>" in str(exc_info.value)


class TestTransformers:
    def test_sanitize_catalog_fields_with_empty_and_missing_keys(self):
        """Проверка очистки каталога с пустыми или некорректными полями."""
        raw_catalog = {
            "id": 42,
            "title": "Тест",
            "fields": [
                {"id": 1, "title": "Field 1", "type": "string"},
                {"id": 2, "title": "Field 2", "type": "select", "options": []}, # Пустые options не должны попадать
            ]
        }
        cleaned = sanitize_catalog_fields(raw_catalog)
        
        assert cleaned["id"] == 42
        assert len(cleaned["fields"]) == 2
        assert "options" not in cleaned["fields"][1]

    def test_sanitize_catalogs_list_filtering(self):
        """Проверка фильтрации тяжелых полей из списка каталогов."""
        raw_catalogs = [
            {"id": 1, "title": "Cat 1", "sectionId": 10, "heavy_metadata": "x" * 1000},
            {"id": 2, "title": "Cat 2", "sectionId": 12, "heavy_metadata": "y" * 1000},
        ]
        result = sanitize_catalogs_list(raw_catalogs)
        
        assert len(result) == 2
        assert result[0] == {"id": 1, "title": "Cat 1", "sectionId": 10}
        assert "heavy_metadata" not in result[0]