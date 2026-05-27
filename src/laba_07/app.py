

from typing import List, Callable, Optional, Union
from .models import Competition, TeamCompetition, IndividualCompetition
from .exceptions import ItemNotFoundError, DuplicateItemError
from .storage import save, load


Predicate = Callable[[Competition], bool]

SortKey = Callable[[Competition], Union[str, int, float]]

class Application:
    def __init__(self, data_file: str = ""):
        self._items: List[Competition] = []
        self._data_file = data_file
        if data_file:
            try:
                self._items = load(data_file)
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self._items = []

    def add_item(self, item: Competition) -> None:
        if self.find_by_id(item.competition_id):
            raise DuplicateItemError(f"Соревнование с ID {item.competition_id} уже существует.")
        self._items.append(item)

    def find_by_id(self, competition_id: str) -> Optional[Competition]:
        for comp in self._items:
            if comp.competition_id == competition_id:
                return comp
        return None

    def get_all(self) -> List[Competition]:
        return self._items.copy()

    def remove_item(self, competition_id: str) -> Competition:
        comp = self.find_by_id(competition_id)
        if comp is None:
            raise ItemNotFoundError(f"Соревнование с ID {competition_id} не найдено.")
        self._items.remove(comp)
        return comp

    def filter_items(self, predicate: Predicate) -> List[Competition]:
        return [comp for comp in self._items if predicate(comp)]

    def sort_items(self, key: SortKey, reverse: bool = False) -> List[Competition]:
        return sorted(self._items, key=key, reverse=reverse)

    def save_data(self) -> None:
        if self._data_file:
            save(self._items, self._data_file)
        else:
            print("[WARN] Путь к файлу данных не указан. Сохранение невозможно.")

    def load_data(self, filepath: str) -> None:
        self._data_file = filepath
        self._items = load(filepath)