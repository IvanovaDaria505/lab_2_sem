"""
Модуль container.py для лабораторной работы №6
Содержит generic-класс TypedCollection и протоколы типизации
"""

from typing import TypeVar, Generic, Callable, Optional, Protocol, Union, List


# ==================== ПРОТОКОЛЫ (ЗАДАНИЕ НА 5) ====================

class Displayable(Protocol):
    """Протокол для объектов с методом display() -> str"""
    def display(self) -> str: ...


class Scorable(Protocol):
    """Протокол для объектов с методом score() -> float"""
    def score(self) -> float: ...


# ==================== TYPE VARIABLES ====================

T = TypeVar('T')
R = TypeVar('R')
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


# ==================== GENERIC КОЛЛЕКЦИЯ ====================

class TypedCollection(Generic[T]):
    """Типизированная коллекция (все методы из ЛР-2 + новые из ЛР-6)"""
    
    def __init__(self, items: Optional[List[T]] = None) -> None:
        self._items: List[T] = items if items is not None else []
    
    # Базовые методы из ЛР-2
    def add(self, item: T) -> None:
        if hasattr(item, 'competition_id') and self.find_by_id(item.competition_id):
            raise ValueError(f"Соревнование с ID {item.competition_id} уже существует в коллекции")
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("Соревнование не найдено в коллекции")
    
    def remove_at(self, index: int) -> T:
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс выходит за границы коллекции")
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def find_by_id(self, competition_id: str) -> Optional[T]:
        for comp in self._items:
            if hasattr(comp, 'competition_id') and comp.competition_id == competition_id:
                return comp
        return None
    
    # Методы поиска из ЛР-2
    def find_by_name(self, name: str) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'name') and comp.name == name])
    
    def find_by_sport_type(self, sport_type: str) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'sport_type') and comp.sport_type == sport_type])
    
    def find_by_location(self, location: str) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'location') and comp.location == location])
    
    def find_by_status(self, status: str) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'status') and comp.status == status])
    
    # Фильтрация по статусу из ЛР-2
    def get_active(self) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'status') and comp.status == "In Progress"])
    
    def get_registration(self) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'status') and comp.status == "Registration"])
    
    def get_completed(self) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'status') and comp.status == "Completed"])
    
    def get_long_duration(self, min_participants: int = 2) -> 'TypedCollection[T]':
        return TypedCollection([comp for comp in self._items 
                               if hasattr(comp, 'max_participants') and comp.max_participants > min_participants])
    
    # Сортировка из ЛР-2
    def sort_by_name(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda comp: comp.name if hasattr(comp, 'name') else "", reverse=reverse)
    
    def sort_by_date(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda comp: comp.start_date if hasattr(comp, 'start_date') else "", reverse=reverse)
    
    def sort_by_duration(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda comp: comp.get_competition_duration() if hasattr(comp, 'get_competition_duration') else 0, reverse=reverse)
    
    def sort_by_participants(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda comp: comp.max_participants if hasattr(comp, 'max_participants') else 0, reverse=reverse)
    
    def sort(self, key: Callable[[T], any], reverse: bool = False) -> None:
        self._items.sort(key=key, reverse=reverse)
    
    # Новые методы из задания на 4
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]
    
    # Методы для протоколов
    def display_all(self) -> None:
        for i, item in enumerate(self._items):
            if hasattr(item, 'display'):
                print(f"[{i}] {item.display()}")
    
    def calculate_average_score(self) -> float:
        if not self._items:
            return 0.0
        scores = [item.score() for item in self._items if hasattr(item, 'score')]
        return sum(scores) / len(scores) if scores else 0.0
    
    # Стандартные методы коллекции
    def __len__(self) -> int:
        return len(self._items)
    
    def __getitem__(self, index: Union[int, slice]) -> Union[T, 'TypedCollection[T]']:
        if isinstance(index, slice):
            return TypedCollection(self._items[index])
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)
    
    def __str__(self) -> str:
        if not self._items:
            return "Коллекция пуста"
        items_str = "\n".join(str(comp) for comp in self._items)
        return f"Коллекция ({len(self)} элементов):\n{items_str}"
    
    def __repr__(self) -> str:
        return f"TypedCollection({len(self._items)} элементов)"