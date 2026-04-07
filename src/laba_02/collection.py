from model import Competition

class CompetitionCollection:

    def __init__(self, items=None):
        self._items = items if items is not None else []

    def add(self, item):
        """Добавление соревнования в коллекцию"""
        if not isinstance(item, Competition):
            raise TypeError("Можно добавлять только объекты типа Competition")
        
        # Проверка на дубликат по ID (как в примере с банковскими счетами)
        if self.find_by_id(item.competition_id):
            raise ValueError("Соревнование с таким ID уже существует в коллекции")
        
        self._items.append(item)
    
    def find_by_id(self, competition_id):
        """Поиск соревнования по ID"""
        for comp in self._items:
            if comp.competition_id == competition_id:
                return comp
        return None
        
    def remove(self, item):
        """Удаление соревнования из коллекции"""
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError("Соревнование не найдено в коллекции")

    def remove_at(self, index):
        """Удаление по индексу"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс выходит за границы коллекции")

    def get_all(self):
        """Получение всех соревнований"""
        return self._items.copy()

    def find_by_name(self, name):
        """Поиск по названию"""
        return CompetitionCollection([comp for comp in self._items if comp.name == name])

    def find_by_sport_type(self, sport_type):
        """Поиск по виду спорта"""
        return CompetitionCollection([comp for comp in self._items if comp.sport_type == sport_type])

    def find_by_location(self, location):
        """Поиск по месту проведения"""
        return CompetitionCollection([comp for comp in self._items if comp.location == location])

    def find_by_status(self, status):
        """Поиск по статусу"""
        return CompetitionCollection([comp for comp in self._items if comp.status == status])

    def get_active(self):
        """Получение активных соревнований"""
        return CompetitionCollection([comp for comp in self._items if comp.status == "In Progress"])

    def get_registration(self):
        """Получение соревнований с открытой регистрацией"""
        return CompetitionCollection([comp for comp in self._items if comp.status == "Registration"])

    def get_completed(self):
        """Получение завершённых соревнований"""
        return CompetitionCollection([comp for comp in self._items if comp.status == "Completed"])

    def get_long_duration(self, min_participants=100):
        """Получение соревнований с большим количеством участников"""
        return CompetitionCollection([comp for comp in self._items if comp.max_participants > min_participants])

    def sort_by_name(self, reverse=False):
        """Сортировка по названию"""
        self._items.sort(key=lambda comp: comp.name, reverse=reverse)

    def sort_by_date(self, reverse=False):
        """Сортировка по дате начала"""
        self._items.sort(key=lambda comp: comp.start_date, reverse=reverse)
    
    def sort_by_duration(self, reverse=False):
        """Сортировка по длительности"""
        self._items.sort(key=lambda comp: comp.get_competition_duration(), reverse=reverse)
    
    def sort_by_participants(self, reverse=False):
        """Сортировка по максимальному количеству участников"""
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