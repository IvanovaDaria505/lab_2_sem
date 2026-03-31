from datetime import datetime
types_of_statues = ['Registration', 'In progress', 'Completed', 'Cancelled']

def validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("Название должно быть строкой") 
    wworld = name.strip()
    if not wworld:  
        raise ValueError("Название соревнования не может быть пустым")
    return wworld


def validate_sport_type(sport_type: str) -> str:
    if not isinstance(sport_type, str):
        raise TypeError("Вид спорта должен быть строкой")
    wworld = sport_type.strip()
   
    if not wworld:
        raise ValueError("Вид спорта не может быть пустым")
    
    if len(wworld) < 1:
        raise ValueError("Название вида спорта слишком короткое")
    
    if len(wworld) > 59:
        raise ValueError("Название вида спорта слишком длинное")
    
    if not wworld.isalpha():
        for c in wworld:
            if not c.isalpha():
                raise ValueError(f"Недопустимый символ '{c}' в названии вида спорта. "
                               f"Разрешены только буквы")
    
    import re
    if re.search(r'[a-zA-Z]', wworld) and re.search(r'[а-яА-Я]', wworld):
        raise ValueError("Нужно использовать только один язык")
    return wworld.capitalize()


def validate_location(location : str) -> str:
    if not isinstance(location, str):
        raise TypeError("Название локации должно быть строкой") 
    wworld = location.strip()
    
    if not wworld:  
        raise ValueError("Название локации не может быть пустым")
    return wworld


def validate_dates(start_date: str, end_date: str) -> tuple:
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Даты должны быть в формате ГГГГ-ММ-ДД")
    
    if end < start:
        raise ValueError("Дата окончания должна быть позже или равна дате начала")

    return start_date, end_date



def validate_max_participants(max_participants: int) -> int:
    if not isinstance(max_participants, int):
        raise TypeError("Максимальное количество участников должно быть целым числом")
   
    if max_participants <= 0:
        raise ValueError("Максимальное количество участников должно быть больше 0")
    return max_participants

def validate_status(status: str) -> str:
    if not isinstance(status, str):
        raise TypeError("Статус должен быть строкой.")
    if status not in types_of_statues:
        raise ValueError(f"Статус должен быть одним из: {', '.join(types_of_statues)}")
    return status

def validate_status_transition(current_status: str, new_status: str) -> bool:
    allowed_transitions = {
        "Registration": ["In Progress", "Cancelled"],
        "In Progress": ["Completed", "Cancelled"],
        "Completed": [],  
        "Cancelled": ["Registration"] 
    }

    if new_status in allowed_transitions.get(current_status, []):
        return True
    else:
        raise ValueError(
            f"Невозможно перейти из статуса '{current_status}' в статус '{new_status}'. "
            f"Допустимые переходы: {allowed_transitions.get(current_status, [])}"
        )

def validate_score(score) -> float:
    if not isinstance(score, (int, float)):
        raise TypeError("Результат должен быть числом")
    
    if score < 0:
        raise ValueError("Результат не может быть отрицательным")
    result = float(score)
    
    if result == float('inf') or result == float('-inf'):
        raise ValueError("Результат не может быть бесконечностью")
    
    return result


def validate_min_participants(participants, min_required: int) -> bool:
    if not isinstance(participants, list):
        raise TypeError('Неправильный формат ввода, введите в формате list')
    
    if not isinstance(min_required, int):
        raise TypeError('Неправильный формат ввода, введите в формате int')

    if min_required < 0:
        raise ValueError("Значение не может быть отрицательным")
    

    for i, p in enumerate(participants):
        if not isinstance(p, str):
            raise TypeError('Неправильный формат ввода')
    
    if len(participants) < min_required:
        raise ValueError(
            f"Недостаточно участников для проведения соревнования.\n"
            f"   Требуется: {min_required}\n"
            f"   Зарегистрировано: {len(participants)}\n"
            f"   Не хватает: {min_required - len(participants)}"
        )
    
    return True