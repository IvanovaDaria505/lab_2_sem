from model import Competition

class CompetitionCollection:

    def __init__(self, items=None):
        self._items = items if items is not None else []

    def add(self, item):
        if not isinstance(item, Competition):
            raise TypeError("Можно добавлять только объекты типа Competition")
        
        if self.find_by_id(item.competition_id):
            raise ValueError("Соревнование с таким ID уже существует в коллекции")
        
        self._items.append(item)
    
    def find_by_id(self, competition_id):
        for comp in self._items:
            if comp.competition_id == competition_id:
                return comp
        return None
        
    def remove(self, item):
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("Соревнование не найдено в коллекции")

    def remove_at(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс выходит за границы коллекции")

    def get_all(self):
        return self._items.copy()

    def find_by_name(self, name):
        return CompetitionCollection([comp for comp in self._items if comp.name == name])

    def find_by_sport_type(self, sport_type):
        return CompetitionCollection([comp for comp in self._items if comp.sport_type == sport_type])

    def find_by_location(self, location):
        return CompetitionCollection([comp for comp in self._items if comp.location == location])

    def find_by_status(self, status):
        return CompetitionCollection([comp for comp in self._items if comp.status == status])

    def get_active(self):
        return CompetitionCollection([comp for comp in self._items if comp.status == "In Progress"])

    def get_registration(self):
        return CompetitionCollection([comp for comp in self._items if comp.status == "Registration"])

    def get_completed(self):
        return CompetitionCollection([comp for comp in self._items if comp.status == "Completed"])

    def get_long_duration(self, min_participants=2):
        return CompetitionCollection([comp for comp in self._items if comp.max_participants > min_participants])

    def sort_by_name(self, reverse=False):
        self._items.sort(key=lambda comp: comp.name, reverse=reverse)

    def sort_by_date(self, reverse=False):
        self._items.sort(key=lambda comp: comp.start_date, reverse=reverse)
    
    def sort_by_duration(self, reverse=False):
        self._items.sort(key=lambda comp: comp.get_competition_duration(), reverse=reverse)
    
    def sort_by_participants(self, reverse=False):
        self._items.sort(key=lambda comp: comp.max_participants, reverse=reverse)
    
    def sort(self, key, reverse=False):
        """Универсальная сортировка"""
        self._items.sort(key=key, reverse=reverse)

    def __len__(self):
        """Возвращает количество соревнований"""
        return len(self._items)

    def __getitem__(self, index):
        """Доступ по индексу и срезам"""
        if isinstance(index, slice):
            return CompetitionCollection(self._items[index])
        return self._items[index]

    def __iter__(self):
        """Итератор по коллекции"""
        return iter(self._items)

    def __str__(self):
        """Строковое представление"""
        if not self._items:
            return "Коллекция пуста"
        competitions_str = "\n".join(str(comp) for comp in self._items)
        return f"Коллекция соревнований ({len(self)} соревнований):\n{competitions_str}"

    def __repr__(self):
        return f"CompetitionCollection({len(self._items)} соревнований)"