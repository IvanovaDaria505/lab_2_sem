"""
Модуль для сохранения и загрузки коллекции соревнований в JSON-файл.
"""
import json
from typing import List, Union
from pathlib import Path
from .exceptions import StorageError
from .models import Competition, TeamCompetition, IndividualCompetition

# Путь к файлу данных по умолчанию
DEFAULT_FILEPATH = Path(__file__).parent.parent.parent / "data" / "competitions.json"

def save(collection: List[Competition], filepath: str = str(DEFAULT_FILEPATH)) -> None:
    """
    Сохранить коллекцию объектов Competition в JSON-файл.
    
    Args:
        collection: Список объектов соревнований.
        filepath: Путь к файлу для сохранения.
    
    Raises:
        StorageError: Если не удалось сохранить файл.
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)  # Создаем папку data, если её нет
        
        data = [comp.to_dict() for comp in collection]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Данные сохранены в {filepath}")
    except Exception as e:
        raise StorageError(f"Не удалось сохранить данные: {e}")

def load(filepath: str = str(DEFAULT_FILEPATH)) -> List[Competition]:
    """
    Загрузить объекты Competition из JSON-файла.
    
    Args:
        filepath: Путь к файлу для загрузки.
    
    Returns:
        Список восстановленных объектов соревнований.
    
    Raises:
        StorageError: Если файл не найден или поврежден.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"  [INFO] Файл данных не найден ({filepath}). Начинаем с пустой коллекции.")
        return []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items: List[Competition] = []
        for item_data in data:
            comp_type = item_data.get("type")
            if comp_type == "TeamCompetition":
                items.append(TeamCompetition.from_dict(item_data))
            elif comp_type == "IndividualCompetition":
                items.append(IndividualCompetition.from_dict(item_data))
            else:
                print(f"  [WARN] Пропущен объект неизвестного типа: {comp_type}")
        return items
    except json.JSONDecodeError as e:
        raise StorageError(f"Ошибка чтения JSON из файла {filepath}: {e}")
    except Exception as e:
        raise StorageError(f"Не удалось загрузить данные: {e}")