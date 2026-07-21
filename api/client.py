from api.exceptions import BpiumClientException
from api.resources import (
    CatalogsResource,
    RecordsResource,
    SectionsResource,
    SystemResource
)
from api.utils import check_response
import httpx

class BpiumClient:
    def __init__(
        self, 
        base_url = 'https://sd-demo.bpium.ru',
        api_url = '/api/v1'
    ):
        headers = {
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(
            follow_redirects=True,
            headers=headers,
            base_url=base_url
        )
        self.catalogs = CatalogsResource(self.client, api_url)
        self.records = RecordsResource(self.client, api_url)
        self.sections = SectionsResource(self.client, api_url)
        self.system = SystemResource(self.client, api_url)
        self._is_closed = False
        self.is_authorized = False

    async def __aenter__(self):
        """Вход в контекстный менеджер"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера - закрываем клиент"""
        await self.close()

    async def close(self):
        """Закрывает HTTP клиент"""
        if not self._is_closed:
            await self.client.aclose()
            self._is_closed = True

    async def login_post(self, email: str, password: str) -> httpx.Response:
        if self.is_authorized == True:
            return
        """
        Авторизация через POST-запрос на /auth/login.
        Сессионные Cookie (например, 'connect.sid') сохраняются внутри httpx.Client.
        """
        url = f"/auth/login"
        payload = {"email": email, "password": password}                
        response = await self.client.post(url, json=payload)
        check_response(response)
        return response