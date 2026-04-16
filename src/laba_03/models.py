# src/lab03/models.py
from base import Competition
from datetime import datetime

class TeamCompetition(Competition):
    
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int,
                 min_teams: int, team_size: int):
        super().__init__(name, sport_type, location, start_date, end_date, max_participants)
        self._min_teams = min_teams
        self._team_size = team_size
        self._registered_teams = [] 

    @property
    def min_teams(self):
        return self._min_teams

    @property
    def team_size(self):
        return self._team_size

    def register_team(self, team_name: str):
        if len(self._registered_teams) >= self._max_participants // self._team_size:
            raise ValueError("Достигнут лимит команд")
        if team_name not in self._registered_teams:
            self._registered_teams.append(team_name)
            for i in range(self._team_size):
                self._participants.append(f"{team_name}_player_{i+1}")
            return True
        return False

    def get_teams_list(self):
        return self._registered_teams.copy()

    def __str__(self):
        base_str = super().__str__()
        lines = base_str.split('\n')
        team_info = f"│ Тип: Командное ({self._min_teams} команд мин.)     │\n"
        team_info += f"│ Заявлено команд: {len(self._registered_teams):<20} │\n"
        
        result_lines = lines[:-1] + [team_info] + [lines[-1]]
        return '\n'.join(result_lines)

    def calculate_organizer_fee(self):
        base_rate = 500.0
        return base_rate * len(self._registered_teams) * 1.5

    def next_status(self):
        if self._status == "Registration":
            if len(self._registered_teams) < self._min_teams:
                return f"Ошибка: нужно минимум {self._min_teams} команд! Сейчас: {len(self._registered_teams)}"
            self._status = "In Progress"
            return f"Командное соревнование началось! Статус: In Progress"
        return super().next_status()


class IndividualCompetition(Competition):
    
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int,
                 category: str, prize_fund: float):
        super().__init__(name, sport_type, location, start_date, end_date, max_participants)
        self._category = category
        self._prize_fund = prize_fund
        self._rating_required = 1000

    @property
    def category(self):
        return self._category

    @property
    def prize_fund(self):
        return self._prize_fund

    def set_rating_requirement(self, rating: int):
        if rating > 0:
            self._rating_required = rating
        else:
            raise ValueError("Рейтинг должен быть положительным")

    def get_rating_requirement(self):
        return self._rating_required

    def __str__(self):
        base_str = super().__str__()
        lines = base_str.split('\n')
        ind_info = f"│ Тип: Индивидуальное ({self._category})         │\n"
        ind_info += f"│ Призовой фонд: {self._prize_fund:>10.2f} руб.   │\n"
        ind_info += f"│ Мин. рейтинг: {self._rating_required:<21} │\n"
        
        result_lines = lines[:-1] + [ind_info] + [lines[-1]]
        return '\n'.join(result_lines)

    def calculate_organizer_fee(self):
        base_fee = 200.0
        rating_coefficient = self._rating_required / 1000.0
        prize_coefficient = self._prize_fund / 10000.0
        return base_fee * rating_coefficient + prize_coefficient


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

    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        return f"Коллекция соревнований ({len(self)} шт.)"

    def filter_by_type(self, comp_type):
        if not isinstance(comp_type, type):
            raise TypeError("comp_type должен быть классом")
        filtered_items = [item for item in self._items if isinstance(item, comp_type)]
        return CompetitionCollection(filtered_items)

    def get_only_team_competitions(self):
        return self.filter_by_type(TeamCompetition)

    def get_only_individual_competitions(self):
        return self.filter_by_type(IndividualCompetition)