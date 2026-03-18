from model import Competition

def demo_validation():
    """Сценарий 1: базовая валидация."""
    print("=== Сценарий 1: Валидация данных ===")
    
    try:
        comp = Competition("", "волейбол", "Москва", "2015-05-03", "2015-05-10", 16)
    except ValueError as e:
        print(f"Ошибка при создании (пустое название): {e}")
    
    try:
        comp = Competition("Турнир", "шахматы123", "Сочи", "2014-06-01", "2014-06-10", 10)
    except ValueError as e:
        print(f"Ошибка при создании (цифры в виде спорта): {e}")
    
    try:
        comp = Competition("Соревнования", "футбол", "Волгоград", "2017-05-23", "2017-05-27", -5)
    except ValueError as e:
        print(f"Ошибка при создании (отрицательные участники): {e}")
    

    comp = Competition("Чемпионат", "футбол", "Москва", "2018-06-01", "2018-06-10", 20)
    print(f"Создано соревнование: {comp}")
    
    # Ошибка при изменении через сеттер
    try:
        comp.location = ""
    except ValueError as e:
        print(f"Ошибка при изменении локации: {e}")
    print()

def demo_state_changes():
    """Сценарий 2: логическое состояние (статусы)."""
    print("=== Сценарий 2: Логическое состояние (статусы) ===")
    
    comp = Competition("Турнир", "теннис", "Сочи", "2024-09-01", "2024-09-05", 8)
    print(f"Начальное состояние: {comp}")
    
    # Пытаемся начать без участников
    print(f"\nПопытка начать без участников:")
    result = comp.next_status()
    print(f"Результат: {result}")
    
    # Добавляем участников
    comp._participants.extend(["Игрок1", "Игрок2", "Игрок3", "Игрок4"])
    print(f"\nДобавлено 4 участника")
    
    # Начинаем соревнование
    print(f"\nЗапуск соревнования:")
    result = comp.next_status()
    print(f"Результат: {result}")
    print(f"Новый статус: {comp.status}")
    
    # Завершаем
    print(f"\nЗавершение соревнования:")
    result = comp.next_status()
    print(f"Результат: {result}")
    print(f"Итоговый статус: {comp.status}")
    
    # Пытаемся изменить завершенное
    print(f"\nПопытка изменить завершенное соревнование:")
    result = comp.next_status()
    print(f"Результат: {result}")
    print()

def demo_equality():
    """Сценарий 3: сравнение объектов."""
    print("=== Сценарий 3: Сравнение и независимость ===")
    
    comp1 = Competition("Кубок", "баскетбол", "Саратов", "2020-06-01", "2020-06-10", 16)
    comp2 = Competition("Кубок", "баскетбол", "Саратов", "2020-06-01", "2020-06-10", 16)
    comp3 = Competition("Чемпионат", "хоккей", "Казань", "2020-12-01", "2020-12-10", 8)
    
    print(f"comp1: {repr(comp1)}")
    print(f"comp2: {repr(comp2)}")
    print(f"comp3: {repr(comp3)}")
    print(f"comp1 == comp2 ? {comp1 == comp2} (разные ID)")
    print(f"comp1 == comp3 ? {comp1 == comp3}")
    
    # Добавляем участников в comp2
    comp2._participants.append("Участник")
    print(f"\nПосле добавления участника в comp2:")
    print(f"comp1 участников: {comp1.participants_count}")
    print(f"comp2 участников: {comp2.participants_count}")
    print(f"comp1 == comp2 ? {comp1 == comp2} (всё ещё разные ID)")
    print()

def demo_class_attribute():
    """Сценарий 4: атрибуты класса."""
    print("=== Сценарий 4: Атрибуты класса ===")
    
    # Доступ через класс
    print(f"Competition.sport_federation = {Competition.sport_federation}")
    print(f"Competition.competition_count = {Competition.competition_count}")
    
    # Создаём экземпляры
    comp1 = Competition("Турнир1", "бокс", "Москва", "2025-07-01", "2025-07-10", 16)
    comp2 = Competition("Турнир2", "теннис", "Сочи", "2024-07-01", "2024-07-05", 8)
    
    print(f"\nСоздано два соревнования:")
    print(f"comp1 ID: {comp1.competition_id}")
    print(f"comp2 ID: {comp2.competition_id}")
    
    # Доступ через экземпляр
    print(f"\nЧерез экземпляр comp1: comp1.sport_federation = {comp1.sport_federation}")
    print(f"Через экземпляр comp2: comp2.sport_federation = {comp2.sport_federation}")
    
    # Изменение атрибута класса
    print(f"\nИзменение атрибута класса:")
    Competition.sport_federation = "Новая федерация"
    print(f"comp1.sport_federation = {comp1.sport_federation}")
    print(f"comp2.sport_federation = {comp2.sport_federation}")
    print(f"Теперь Competition.competition_count = {Competition.competition_count}")
    print()

def demo_multiple_states():
    """Сценарий 5: множественные состояния."""
    print("=== Сценарий 5: Множественные состояния ===")
    
    comp = Competition("Чемпионат", "баскетбол", "Краснодар", "2024-10-01", "2024-10-07", 8)
    print(f"Исходное соревнование:\n{comp}")
    
    # Состояние 1: Регистрация (мало участников)
    print(f"\n▶ Состояние: {comp.status}")
    print(f"Участников: {comp.participants_count}, нужно минимум: {comp.min_participants}")
    
    # Пытаемся начать
    result = comp.next_status()
    print(f"Попытка начать: {result}")
    
    # Состояние 2: Добавляем участников
    print(f"\n▶ Добавляем участников...")
    comp._participants.extend(["Игрок1", "Игрок2", "Игрок3", "Игрок4"])
    print(f"Теперь участников: {comp.participants_count}")
    
    # Начинаем
    result = comp.next_status()
    print(f"Запуск: {result}")
    print(f"Новый статус: {comp.status}")
    
    # Состояние 3: В процессе
    print(f"\n▶ Состояние: {comp.status}")
    print(f"Участники: {comp.participants}")
    
    # Завершаем
    result = comp.next_status()
    print(f"Завершение: {result}")
    print(f"Новый статус: {comp.status}")
    
    # Состояние 4: Завершено
    print(f"\n▶ Состояние: {comp.status}")
    print(f"Пытаемся изменить статус завершенного соревнования:")
    result = comp.next_status()
    print(f"Результат: {result}")
    
    # Состояние 5: Проверка валидации перехода
    print(f"\n▶ Проверка недопустимого перехода:")
    try:
        from validate import validate_status_transition
        validate_status_transition("Completed", "Registration")
    except ValueError as e:
        print(f"Ошибка: {e}")
    print()

def demo_date_operations():
    """Сценарий 6: работа с датами."""
    print("=== Сценарий 6: Работа с датами ===")
    
    # Создание короткого соревнования
    comp_short = Competition(
        name="Спринт",
        sport_type="бег",
        location="Москва",
        start_date="2024-05-01",
        end_date="2024-05-03",
        max_participants=10
    )
    print(f"\nКороткое соревнование:")
    print(f"  Название: {comp_short.name}")
    print(f"  Даты: {comp_short.start_date} - {comp_short.end_date}")
    print(f"  Длительность: {comp_short.get_competition_duration()} дней")
    
    # Создание длинного соревнования
    comp_long = Competition(
        name="Марафон",
        sport_type="бег",
        location="Москва",
        start_date="2024-06-01",
        end_date="2024-06-30",
        max_participants=50
    )
    print(f"\nДлинное соревнование:")
    print(f"  Название: {comp_long.name}")
    print(f"  Даты: {comp_long.start_date} - {comp_long.end_date}")
    print(f"  Длительность: {comp_long.get_competition_duration()} дней")
    
    # Сравнение длительностей
    print(f"\n▶ Сравнение длительностей:")
    print(f"  {comp_short.name} короче чем {comp_long.name}?")
    print(f"  {comp_short.get_competition_duration()} < {comp_long.get_competition_duration()} → {comp_short.get_competition_duration() < comp_long.get_competition_duration()}")
    print()

def demo_magic_methods():
    """Сценарий 7: магические методы."""
    print("=== Сценарий 7: Магические методы ===")
    
    # __str__ - пользовательский вывод
    print("\n▶ __str__ (для пользователей):")
    comp = Competition(
        name="Чемпионат мира",
        sport_type="футбол",
        location="Москва",
        start_date="2024-06-01",
        end_date="2024-06-30",
        max_participants=32
    )
    comp._participants.extend(["Россия", "Бразилия", "Германия", "Аргентина"])
    print(comp)
    
    # __repr__ - отладочный вывод
    print("\n▶ __repr__ (для разработчиков):")
    print(repr(comp))
    
    # __eq__ - сравнение по ID
    print("\n▶ __eq__ (сравнение по ID):")
    comp_same = Competition(
        name="Чемпионат мира",
        sport_type="футбол",
        location="Москва",
        start_date="2024-06-01",
        end_date="2024-06-30",
        max_participants=32
    )
    comp_diff = Competition(
        name="Кубок",
        sport_type="хоккей",
        location="Казань",
        start_date="2024-12-01",
        end_date="2024-12-10",
        max_participants=8
    )
    print(f"  comp == comp_same: {comp == comp_same} (разные ID: {comp.competition_id} vs {comp_same.competition_id})")
    print(f"  comp == comp_diff: {comp == comp_diff}")
    print(f"  comp == comp: {comp == comp} (одинаковый ID)")
    
    # Сравнение по длительности (аналог lt)
    print("\n▶ Сравнение по длительности:")
    comp_short = Competition("Спринт", "бег", "Москва", "2024-05-01", "2024-05-03", 10)
    comp_long = Competition("Марафон", "бег", "Москва", "2024-06-01", "2024-06-30", 50)
    
    print(f"  {comp_short.name}: {comp_short.get_competition_duration()} дней")
    print(f"  {comp_long.name}: {comp_long.get_competition_duration()} дней")
    print(f"  {comp_short.name} < {comp_long.name}? {comp_short.get_competition_duration() < comp_long.get_competition_duration()}")
    print(f"  {comp_long.name} < {comp_short.name}? {comp_long.get_competition_duration() < comp_short.get_competition_duration()}")
    
    # Сортировка списка соревнований по длительности
    print("\n▶ Сортировка соревнований по длительности:")
    competitions = [comp_long, comp_short, comp]
    print("  До сортировки:")
    for c in competitions:
        print(f"    {c.name}: {c.get_competition_duration()} дней")
    
    competitions.sort(key=lambda x: x.get_competition_duration())
    print("  После сортировки (по возрастанию длительности):")
    for c in competitions:
        print(f"    {c.name}: {c.get_competition_duration()} дней")
    print()

if __name__ == "__main__":
    demo_validation()
    demo_state_changes()
    demo_equality()
    demo_class_attribute()
    demo_multiple_states()
    demo_date_operations()
    demo_magic_methods()