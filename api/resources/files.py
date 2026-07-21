import json
from typing import Any, Dict, List, Optional
from api.base import BaseResource
from api.utils import check_response

class FilesResource(BaseResource):
    async def download_file(self, file_id: int) -> httpx.Response:
        """Скачать файл по его ID."""
        url = f"{self.api_url}/files/{file_id}"
        response = await self.client.get(url)
        check_response(response)
        return response

    async def upload_file_to_storage(
        self, 
        catalog_id: int, 
        field_id: int, 
        file_name: str, 
        file_content: bytes, 
        mime_type: str,
        record_id: Optional[int] = None
    ) -> int:
        """
        Полный цикл загрузки файла в хранилище Bpium (Шаги 1-3).
        Возвращает ID созданного файла для последующего прикрепления к записи.
        """
        # Шаг 1: Получение ключей доступа к хранилищу
        init_url = f"{self.api_url}/files/"
        init_payload = {
            "catalogId": str(catalog_id),
            "fieldId": str(field_id),
            "name": file_name,
            "size": len(file_content),
            "mimeType": mime_type,
            "typeStorage": "remoteStorage"
        }
        if record_id is not None:
            init_payload["recordId"] = str(record_id)

        init_res = await self.client.post(init_url, json=init_payload)
        check_response(init_res)
        credentials = init_res.json()

        file_id = credentials["fileId"]
        upload_url = credentials["uploadUrl"]

        # Шаг 2: Загрузка бинарника в хранилище (S3-совместимое) через Multipart
        # Важно передать параметры строго в соответствии с требованиями API (включая "police" вместо "policy")
        upload_data = {
            "key": credentials["fileKey"],
            "acl": "private",
            "AWSAccessKeyId": credentials["AWSAccessKeyId"],
            "Policy": credentials["police"],  # Опечатка в API документации Bpium: police!!!
            "Signature": credentials["signature"],
            "Content-Type": mime_type
        }
        
        # Передаем файл как бинарные данные в multipart
        files = {"file": (file_name, file_content, mime_type)}

        # Внешний запрос к хранилищу, заголовки авторизации Bpium здесь не нужны
        with httpx.Client() as storage_client:
            storage_res = storage_client.post(upload_url, data=upload_data, files=files)
            if not storage_res.is_success:
                raise BpiumClientException(
                    storage_res.status_code, 
                    f"Ошибка S3-хранилища при загрузке: {storage_res.text}"
                )

        # Шаг 3: Подтверждение загрузки файла на сервере Bpium
        confirm_url = f"{self.api_url}/files/{file_id}"
        confirm_payload = {
            "fileId": file_id,
            "name": file_name,
            "size": len(file_content),
            "mimeType": mime_type,
            "url": credentials.get("url", "")  # Путь к файлу из Шага 1
        }
        
        confirm_res = await self.client.patch(confirm_url, json=confirm_payload)
        check_response(confirm_res)

        return file_id
