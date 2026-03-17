from model import Competition
import validate

print("1 сценарий работы")
    
    # Создание объекта
print("\n1. Создание объекта Competition:")
comp = Competition(
        name="Олимпиада",
        sport_type="Биатлон",
        location="Сочи",
        start_date="2014-06-01",
        end_date="2014-06-30",
        max_participants=32
    )
print(comp)
    
print("\n2. Добавление участников:")
comp._participants.append("Сборная России")
comp._participants.append("Сборная Аргентины")
comp._participants.append("Сборная Германии")
print(f"   Участники: {comp.participants}")
print(f"   Количество: {comp.participants_count}")
    
print("\n3. Бизнес-метод (get_participants_list):")
print(comp.get_participants_list())
    
print("\n4. Сравнение объектов (__eq__):")
comp2 = Competition(
        name="Чемпионат Европы",
        sport_type="Биатлон",
        location="Минск",
        start_date="2015-07-01",
        end_date="2015-07-15",
        max_participants=16
    )
print(f"   comp == comp2: {comp == comp2}")
print(f"   comp == comp: {comp == comp}")
    
    # СЦЕНАРИЙ 2: ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ
print("\n" + "-" * 40)
print("▶ СЦЕНАРИЙ 2: Демонстрация валидации")
print("-" * 40)
    
    print("\n1. Ошибка: пустое название")
    try:
        comp_invalid = Competition(
            name="",
            sport_type="Волейбол",
            location="Москва",
            start_date="2016-08-01",
            end_date="2016-08-10",
            max_participants=10
        )
    except (ValueError, TypeError) as e:
        print(f"   → {e}")
    
    print("\n2. Ошибка: дата окончания раньше даты начала")
    try:
        comp_invalid = Competition(
            name="Матч между командами Казани и Волгограда",
            sport_type="баскетбол",
            location="Казань",
            start_date="2017-09-10",
            end_date="2017-09-01",
            max_participants=10
        )
    except (ValueError, TypeError) as e:
        print(f"   → {e}")
    
    print("\n3. Ошибка: отрицательное количество участников")
    try:
        comp_invalid = Competition(
            name="Турнир",
            sport_type="волейбол",
            location="Сочи",
            start_date="2024-10-01",
            end_date="2024-10-05",
            max_participants=-5
        )
    except (ValueError, TypeError) as e:
        print(f"   → {e}")
    
    # =========================================================
    # СЦЕНАРИЙ 3: ИЗМЕНЕНИЕ СОСТОЯНИЯ И ЛОГИЧЕСКИЕ ОГРАНИЧЕНИЯ
    # =========================================================
    print("\n" + "-" * 40)
    print("▶ СЦЕНАРИЙ 3: Изменение состояния и логические ограничения")
    print("-" * 40)
    
    # Создаем новое соревнование
    comp3 = Competition(
        name="Теннисный турнир",
        sport_type="теннис",
        location="Корт 1",
        start_date="2024-07-01",
        end_date="2024-07-03",
        max_participants=4
    )
    
    print("\n1. Начальное состояние:")
    print(f"   Статус: {comp3.status}")
    print(f"   Участников: {comp3.participants_count}")
    
    # Пытаемся изменить статус без участников
    print("\n2. Попытка начать соревнование без участников:")
    result = comp3.next_status()
    print(f"   → {result}")
    print(f"   Статус остался: {comp3.status}")
    
    # Добавляем участников
    print("\n3. Добавляем участников:")
    comp3._participants.append("Игрок 1")
    comp3._participants.append("Игрок 2")
    print(f"   Теперь участников: {comp3.participants_count}")
    
    # Начинаем соревнование
    print("\n4. Начинаем соревнование (Registration → In Progress):")
    result = comp3.next_status()
    print(f"   → {result}")
    print(f"   Новый статус: {comp3.status}")
    
    # Пытаемся добавить участника после начала (логическое ограничение)
    print("\n5. Попытка добавить участника после начала соревнования:")
    if comp3.status != "Registration":
        print(f"   → Нельзя добавить участника в статусе '{comp3.status}'")
    
    # Завершаем соревнование
    print("\n6. Завершаем соревнование (In Progress → Completed):")
    result = comp3.next_status()
    print(f"   → {result}")
    print(f"   Новый статус: {comp3.status}")
    
    # Пытаемся завершить еще раз
    print("\n7. Попытка завершить уже завершенное соревнование:")
    result = comp3.next_status()
    print(f"   → {result}")
    
    # =========================================================
    # СЦЕНАРИЙ 4: РАБОТА С РАЗНЫМИ СТАТУСАМИ
    # =========================================================
    print("\n" + "-" * 40)
    print("▶ СЦЕНАРИЙ 4: Работа с разными статусами")
    print("-" * 40)
    
    # Создаем несколько соревнований в разных статусах
    print("\n1. Создаем соревнования в разных статусах:")
    
    reg_comp = Competition(
        name="Турнир А",
        sport_type="шахматы",
        location="Зал 1",
        start_date="2024-11-01",
        end_date="2024-11-03",
        max_participants=8
    )
    print(f"   • {reg_comp.name} - статус: {reg_comp.status}")
    
    prog_comp = Competition(
        name="Турнир Б",
        sport_type="шахматы",
        location="Зал 2",
        start_date="2024-11-05",
        end_date="2024-11-07",
        max_participants=8
    )
    prog_comp._status = "In Progress"
    print(f"   • {prog_comp.name} - статус: {prog_comp.status}")
    
    comp_comp = Competition(
        name="Турнир В",
        sport_type="шахматы",
        location="Зал 3",
        start_date="2024-11-10",
        end_date="2024-11-12",
        max_participants=8
    )
    comp_comp._status = "Completed"
    print(f"   • {comp_comp.name} - статус: {comp_comp.status}")
    
    # Показываем, как один метод по-разному работает
    print("\n2. Один метод next_status() работает по-разному:")
    
    print(f"\n   Для Registration ({reg_comp.status}):")
    print(f"   {reg_comp.next_status()}")
    
    print(f"\n   Для In Progress ({prog_comp.status}):")
    print(f"   {prog_comp.next_status()}")
    
    print(f"\n   Для Completed ({comp_comp.status}):")
    print(f"   {comp_comp.next_status()}")
    
    # =========================================================
    # ИТОГ
    # =========================================================
    print_separator("ИТОГ")
    print("✅ Демонстрация работы класса Competition выполнена!")
    print("\n   Реализовано:")
    print("   • 4 закрытых атрибута (name, sport_type, location, max_participants)")
    print("   • Конструктор с валидацией")
    print("   • Свойства @property")
    print("   • Магические методы: __str__, __repr__, __eq__")
    print("   • 2 бизнес-метода")
    print("   • Метод изменения состояния (next_status)")
    print("   • Поведение, зависящее от статуса")
    print(f"\n📊 Всего создано соревнований: {Competition.competition_count}")


if __name__ == "__main__":
    main()