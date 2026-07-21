class BpiumClientException(Exception):
    """Базовое исключение для ошибок Bpium API."""
    def __init__(self, status_code: int, message: str):
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code