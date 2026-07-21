# transformers.py
from typing import Dict, Any, List

def sanitize_catalog_fields(raw_catalog: Dict[str, Any]) -> Dict[str, Any]:
    """
    Оставляет только минимально необходимые данные о каталоге и его полях,
    экономя контекстное окно LLM.
    """
    raw_fields = raw_catalog.get("fields", [])
    clean_fields = []

    for f in raw_fields:
        field_data = {
            "id": f.get("id"),
            "title": f.get("title"),
            "type": f.get("type"),
        }
        # Если у поля есть варианты выбора (enum / select)
        if "options" in f and f["options"]:
            field_data["options"] = f["options"]
            
        clean_fields.append(field_data)

    return {
        "id": raw_catalog.get("id"),
        "title": raw_catalog.get("title"),
        "fields": clean_fields
    }

def sanitize_catalogs_list(raw_catalogs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает компактный список каталогов без вложенных полей."""
    return [
        {
            "id": cat.get("id"),
            "title": cat.get("title"),
            "sectionId": cat.get("sectionId")
        }
        for cat in raw_catalogs
    ]