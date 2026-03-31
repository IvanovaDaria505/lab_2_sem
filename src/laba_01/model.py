from datetime import datetime
import validate

class Competition:
  
    # Атрибуты класса
    sport_federation = "International Sports Federation (ISF)"
    competition_count = 0
    
    def __init__(self, name: str, sport_type: str, location: str, 
                 start_date: str, end_date: str, max_participants: int):
    
        self._name = validate.validate_name(name)
        self._sport_type = validate.validate_sport_type(sport_type)
        self._location = validate.validate_location(location)
        start, end = validate.validate_dates(start_date, end_date)
        self._start_date = start
        self._end_date = end
        self._max_participants = validate.validate_max_participants(max_participants)
        
        # Дополнительные закрытые атрибуты
        self._status = "Registration"  
        self._participants = [] 
        self._results = {}  
        self._min_participants = 2 
        
        Competition.competition_count += 1
        self._competition_id = f"COMP-{Competition.competition_count:03d}"
    
    # Свойства (геттеры)
    @property
    def name(self):
        """Название соревнования """
        return self._name
    
    @property
    def sport_type(self):
        """Вид спорта """
        return self._sport_type
    
    @property
    def location(self):
        """Место проведения"""
        return self._location
    
    @location.setter
    def location(self, new_location: str):
        """Сеттер для места проведения с валидацией"""
        self._location = validate.validate_location(new_location)
    
    @property
    def start_date(self):
        """Дата начала """
        return self._start_date
    
    @property
    def end_date(self):
        """Дата окончания """
        return self._end_date
    
    @property
    def max_participants(self):
        """Максимальное количество участников """
        return self._max_participants
    
    @property
    def status(self):
        """Статус соревнования """
        return self._status
    
    @property
    def participants(self):
        """Список участников """
        return self._participants.copy()
    
    @property
    def competition_id(self):
        """ID соревнования """
        return self._competition_id
    
    @property
    def participants_count(self):
        """Количество зарегистрированных участников"""
        return len(self._participants)
    
    # Свойство с сеттером
    @property
    def min_participants(self):
        """Минимальное количество участников для проведения"""
        return self._min_participants
    
    @min_participants.setter
    def min_participants(self, value: int):
        """Сеттер для минимального количества участников"""
        validate.validate_min_participants(self._participants, value)
        self._min_participants = value
    
    # Бизнес-методы
    def get_participants_list(self):
    
        if not self._participants:
            return "Нет зарегистрированных участников"
        
        result = "Список участников:\n"
        for i, participant in enumerate(self._participants, 1):
            result += f"  {i}. {participant}\n"
        return result
    


    def get_competition_duration(self):
       
        start = datetime.strptime(self._start_date, "%Y-%m-%d")
        end = datetime.strptime(self._end_date, "%Y-%m-%d")
        duration = (end - start).days
        return duration
    
   
    def next_status(self):
       
        if self._status == "Registration":
            if len(self._participants) < self._min_participants:
                return f"Ошибка: нужно минимум {self._min_participants} участника! Сейчас: {len(self._participants)}"
            self._status = "In Progress"
            return f"Соревнование началось! Статус: In Progress"
            
        elif self._status == "In Progress":
            self._status = "Completed"
            return f"Соревнование завершено! Статус: Completed"
            
        elif self._status == "Completed":
            return "Ошибка: соревнование уже завершено, нельзя изменить статус"
            
        elif self._status == "Cancelled":
            return "Ошибка: соревнование отменено, нельзя изменить статус"
            
        return "Ошибка: неизвестный статус"
    
    # Магические методы
    def __str__(self):
     
        start = datetime.strptime(self._start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        end = datetime.strptime(self._end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        duration = self.get_competition_duration()
        
        return (f"┌────────────────────────────────────┐\n"
                f"│ СОРЕВНОВАНИЕ: {self._name:<25} │\n"
                f"├────────────────────────────────────┤\n"
                f"│ ID: {self._competition_id:<30} │\n"
                f"│ Вид спорта: {self._sport_type:<23} │\n"
                f"│ Место: {self._location:<28} │\n"
                f"│ Даты: {start} - {end:<17} │\n"
                f"│ Длительность: {duration} дн.                 │\n"
                f"│ Участники: {self.participants_count:>3} / {self._max_participants:<3}               │\n"
                f"│ Статус: {self._status:<27} │\n"
                f"└────────────────────────────────────┘")
    
    def __repr__(self):
        
        return (f"Competition(name='{self._name}', sport_type='{self._sport_type}', "
                f"location='{self._location}', participants={self.participants_count})")
    
    def __eq__(self, other):
       
        if not isinstance(other, Competition):
            return False
        return self._competition_id == other._competition_id