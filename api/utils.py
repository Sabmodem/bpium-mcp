import httpx
from api.exceptions import BpiumClientException

def check_response(response: httpx.Response) -> None:
    """Внутренний хендлер для проверки статус-кодов ответов Bpium."""
    if response.is_success:
        return

    status_code = response.status_code
    error_map = {
        400: "Некорректный запрос (Bad Request)",
        401: "Ошибка авторизации (Unauthorized)",
        402: "Требуется оплата лицензии",
        403: "Доступ запрещён (Forbidden)",
        404: "Ресурс не найден (Not Found)",
        405: "Метод не разрешён",
        426: "Требуется расширение лицензии",
        429: "Превышен лимит запросов (Too Many Requests)",
        500: "Внутренняя ошибка сервера (Internal Server Error)",
        501: "Метод не реализован"
    }

    error_message = error_map.get(status_code, "Неизвестная ошибка")
    try:
        detail = response.json()
        error_message = f"{error_message} | Детали: {detail}"
    except Exception:
        error_message = f"{error_message} | Тело ответа: {response.text}"

    raise BpiumClientException(status_code, error_message)