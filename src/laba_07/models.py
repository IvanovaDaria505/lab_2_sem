"""
Модели данных предметной области «Соревнования».
Объединяет классы из ЛР-3 (наследование) и ЛР-4 (интерфейсы).
Добавлены методы to_dict()/from_dict() для сохранения в JSON (ЛР-7).
"""

from datetime import datetime
from abc import ABC, abstractmethod
from typing import Any, List


class Printable(ABC):
    """Интерфейс для объектов, которые можно представить в виде строки."""
    @abstractmethod
    def to_string(self) -> str:
        pass

class Comparable(ABC):
    """Интерфейс для сравнения объектов."""
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        pass

class Competition:
    """
    Базовый класс для всех соревнований.
    Атрибуты класса, валидация, свойства и бизнес-методы из ЛР-1 и ЛР-2.
    """
    sport_federation = "International Sports Federation (ISF)"
    competition_count = 0
    
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int):
        # Простейшая валидация внутри класса для автономности
        if not name.strip(): raise ValueError("Название не может быть пустым")
        self._name = name.strip()
        self._sport_type = sport_type
        self._location = location
        self._start_date = start_date
        self._end_date = end_date
        self._max_participants = max_participants
        
        self._status = "Registration"  
        self._participants: List[str] = []
        self._min_participants = 2 
        
        Competition.competition_count += 1
        self._competition_id = f"COMP-{Competition.competition_count:03d}"
    
    # --- Свойства ---
    @property
    def name(self) -> str: return self._name
    @property
    def sport_type(self) -> str: return self._sport_type
    @property
    def location(self) -> str: return self._location
    @location.setter
    def location(self, new_location: str): self._location = new_location
    @property
    def start_date(self) -> str: return self._start_date
    @property
    def end_date(self) -> str: return self._end_date
    @property
    def max_participants(self) -> int: return self._max_participants
    @property
    def status(self) -> str: return self._status
    @property
    def competition_id(self) -> str: return self._competition_id
    @property
    def participants_count(self) -> int: return len(self._participants)

    # --- Бизнес-методы ---
    def get_competition_duration(self) -> int:
        """Вычисляет длительность соревнования в днях."""
        start = datetime.strptime(self._start_date, "%Y-%m-%d")
        end = datetime.strptime(self._end_date, "%Y-%m-%d")
        return (end - start).days

    def next_status(self) -> str:
        """Переключает статус соревнования."""
        if self._status == "Registration":
            if len(self._participants) < self._min_participants:
                return f"Ошибка: нужно минимум {self._min_participants} участника!"
            self._status = "In Progress"
            return "Соревнование началось!"
        elif self._status == "In Progress":
            self._status = "Completed"
            return "Соревнование завершено!"
        elif self._status == "Completed":
            return "Ошибка: соревнование уже завершено."
        return "Ошибка: неизвестный статус"

    def calculate_organizer_fee(self) -> float:
        """Базовая стоимость организационного взноса."""
        return 0.0

    # --- Магические методы ---
    def __str__(self):
        start = datetime.strptime(self._start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        end = datetime.strptime(self._end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        return (f"[{self._competition_id}] {self._name} ({self._sport_type}) | "
                f"{self._location} | {start} - {end} | Статус: {self._status}")

    def __repr__(self):
        return f"Competition(name='{self._name}')"
    
    def __eq__(self, other):
        if not isinstance(other, Competition):
            return False
        return self._competition_id == other._competition_id

    # --- Методы для сериализации (ЛР-7) ---
    def to_dict(self) -> dict:
        """Сериализует объект в словарь для сохранения в JSON."""
        return {
            "type": self.__class__.__name__,
            "name": self._name,
            "sport_type": self._sport_type,
            "location": self._location,
            "start_date": self._start_date,
            "end_date": self._end_date,
            "max_participants": self._max_participants,
            "status": self._status,
            "competition_id": self._competition_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Competition':
        """Создает объект из словаря (десериализация)."""
        raise NotImplementedError("Этот метод должен быть переопределен в дочерних классах")


class TeamCompetition(Competition, Printable, Comparable):
    """Класс для командных соревнований (из ЛР-3 и ЛР-4)."""
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int,
                 min_teams: int, team_size: int):
        super().__init__(name, sport_type, location, start_date, end_date, max_participants)
        self._min_teams = min_teams
        self._team_size = team_size
        self._registered_teams: List[str] = []

    def register_team(self, team_name: str):
        self._registered_teams.append(team_name)
        self._participants.append(team_name) # Упрощение

    def get_teams_list(self) -> List[str]:
        return self._registered_teams.copy()

    def calculate_organizer_fee(self) -> float:
        return 500.0 * len(self._registered_teams)

    def to_string(self) -> str:
        return f"[КОМАНДНОЕ] {self._name} | Команд: {len(self._registered_teams)}"

    def compare_to(self, other: 'TeamCompetition') -> int:
        if not isinstance(other, TeamCompetition): raise TypeError
        return len(self._registered_teams) - len(other._registered_teams)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "min_teams": self._min_teams,
            "team_size": self._team_size,
            "registered_teams": self._registered_teams
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'TeamCompetition':
        comp = cls(data['name'], data['sport_type'], data['location'],
                   data['start_date'], data['end_date'], data['max_participants'],
                   data['min_teams'], data['team_size'])
        comp._status = data.get('status', 'Registration')
        comp._competition_id = data.get('competition_id', comp._competition_id)
        comp._registered_teams = data.get('registered_teams', [])
        comp._participants = comp._registered_teams.copy()
        return comp

class IndividualCompetition(Competition, Printable, Comparable):
    """Класс для индивидуальных соревнований (из ЛР-3 и ЛР-4)."""
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int,
                 category: str, prize_fund: float):
        super().__init__(name, sport_type, location, start_date, end_date, max_participants)
        self._category = category
        self._prize_fund = prize_fund

    @property
    def prize_fund(self) -> float: return self._prize_fund
    @property
    def category(self) -> str: return self._category

    def calculate_organizer_fee(self) -> float:
        return self._prize_fund * 0.1

    def to_string(self) -> str:
        return f"[ИНДИВИДУАЛЬНОЕ] {self._name} | Призовой фонд: {self._prize_fund:,.0f} руб."

    def compare_to(self, other: 'IndividualCompetition') -> int:
        if not isinstance(other, IndividualCompetition): raise TypeError
        if self._prize_fund < other._prize_fund: return -1
        elif self._prize_fund > other._prize_fund: return 1
        return 0

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "category": self._category,
            "prize_fund": self._prize_fund
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'IndividualCompetition':
        comp = cls(data['name'], data['sport_type'], data['location'],
                   data['start_date'], data['end_date'], data['max_participants'],
                   data['category'], data['prize_fund'])
        comp._status = data.get('status', 'Registration')
        comp._competition_id = data.get('competition_id', comp._competition_id)
        return comp