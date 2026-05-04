import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'laba_03'))
from base import Competition

class CompetitionCollection:
    def __init__(self, items=None):
        self._items = items if items is not None else []

    def add(self, item):
        if not isinstance(item, Competition):
            raise TypeError("Можно добавлять только объекты типа Competition")
        if self.find_by_id(item.competition_id):
            raise ValueError("Соревнование с таким ID уже существует")
        self._items.append(item)
    
    def find_by_id(self, competition_id):
        for comp in self._items:
            if comp.competition_id == competition_id:
                return comp
        return None

    def get_all(self):
        return self._items.copy()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        header = f"=== Коллекция соревнований ({len(self)} шт.) ==="
        items_str = "\n".join(str(item) for item in self._items)
        return f"{header}\n{items_str}"
    
    def sort_by(self, key_func, reverse=False):
        self._items.sort(key=key_func, reverse=reverse)
        return self

    def filter_by(self, predicate):
        filtered = [item for item in self._items if predicate(item)]
        return CompetitionCollection(filtered)

    def apply(self, func):
        for i in range(len(self._items)):
            self._items[i] = func(self._items[i])
        return self

    def filter_by_type(self, comp_type):
        if not isinstance(comp_type, type):
            raise TypeError("comp_type должен быть классом")
        filtered_items = [item for item in self._items if isinstance(item, comp_type)]
        return CompetitionCollection(filtered_items)