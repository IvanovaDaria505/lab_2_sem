"""
Слой бизнес-логики приложения.
Оперирует коллекцией соревнований и предоставляет API для CLI.
Все методы аннотированы типами (ЛР-6, ЛР-7).
"""

from typing import List, Callable, Optional, Union
from .models import Competition, TeamCompetition, IndividualCompetition
from .exceptions import ItemNotFoundError, DuplicateItemError
from .storage import save, load

# Тип для предикатов (из ЛР-5)
Predicate = Callable[[Competition], bool]
# Тип для ключей сортировки
SortKey = Callable[[Competition], Union[str, int, float]]

class Application:
    """
    Главный класс приложения. Управляет коллекцией соревнований.
    """
    def __init__(self, data_file: str = ""):
        self._items: List[Competition] = []
        self._data_file = data_file
        # Попытка автоматической загрузки при старте
        if data_file:
            try:
                self._items = load(data_file)
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self._items = []

    def add_item(self, item: Competition) -> None:
        """
        Добавить соревнование в коллекцию.
        
        Raises:
            DuplicateItemError: Если элемент с таким ID уже существует.
        """
        if self.find_by_id(item.competition_id):
            raise DuplicateItemError(f"Соревнование с ID {item.competition_id} уже существует.")
        self._items.append(item)

    def find_by_id(self, competition_id: str) -> Optional[Competition]:
        """Найти соревнование по его ID."""
        for comp in self._items:
            if comp.competition_id == competition_id:
                return comp
        return None

    def get_all(self) -> List[Competition]:
        """Получить все соревнования."""
        return self._items.copy()

    def remove_item(self, competition_id: str) -> Competition:
        """
        Удалить соревнование по ID.
        
        Raises:
            ItemNotFoundError: Если соревнование не найдено.
        """
        comp = self.find_by_id(competition_id)
        if comp is None:
            raise ItemNotFoundError(f"Соревнование с ID {competition_id} не найдено.")
        self._items.remove(comp)
        return comp

    def filter_items(self, predicate: Predicate) -> List[Competition]:
        """Фильтрация соревнований по предикату."""
        return [comp for comp in self._items if predicate(comp)]

    def sort_items(self, key: SortKey, reverse: bool = False) -> List[Competition]:
        """Сортировка соревнований по ключу."""
        return sorted(self._items, key=key, reverse=reverse)

    def save_data(self) -> None:
        """Сохранить текущее состояние в файл."""
        if self._data_file:
            save(self._items, self._data_file)
        else:
            print("[WARN] Путь к файлу данных не указан. Сохранение невозможно.")

    def load_data(self, filepath: str) -> None:
        """Загрузить данные из файла."""
        self._data_file = filepath
        self._items = load(filepath)