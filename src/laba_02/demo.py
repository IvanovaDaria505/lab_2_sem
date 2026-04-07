from model import Competition
from collection import CompetitionCollection

def print_header(title):
    """Вывод заголовка раздела"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def create_sample_competitions():
    """Создание тестовых соревнований"""
    
    comp1 = Competition(
        "Чемпионат мира по футболу",
        "Футбол",
        "Москва",
        "2018-06-15",
        "2018-07-15",
        32
    )
    
    comp2 = Competition(
        "Олимпийские игры",
        "Биатлон",
        "Париж",
        "2022-07-26",
        "2022-08-11",
        10000
    )
    
    comp3 = Competition(
        "Турнир по теннису",
        "Теннис",
        "Лондон",
        "2016-08-01",
        "2016-08-15",
        128
    )
    
    comp4 = Competition(
        "Чемпионат Европы по баскетболу",
        "Баскетбол",
        "Берлин",
        "2024-09-01",
        "2024-09-18",
        24
    )
    
    comp5 = Competition(
        "Марафон",
        "Бег",
        "Бостон",
        "2026-04-15",
        "2026-04-15",
        30000
    )
    
    comp6 = Competition(
        "Кубок мира по лыжам",
        "Лыжи",
        "Сочи",
        "2024-12-10",
        "2024-12-20",
        150
    )
    
    return [comp1, comp2, comp3, comp4, comp5, comp6]


def scenario_1_basic_operations():
    """Сценарий 1: Базовые операции (add, remove, get_all)"""
    print_header("Сценарий 1: Реализация методов: add, remove, get_all")
    
    collection = CompetitionCollection()
    competitions = create_sample_competitions()

    
    print("1. Создание и добавление соревнований в коллекцию:")
    for comp in competitions[:4]:  
        collection.add(comp)
        print(f"   Добавлено: {comp.name} (ID: {comp.competition_id})")
    
    print(f"\n2. Вывод всех элементов коллекции (всего {len(collection)} соревнований):")
    for comp in collection:
        print(f"   - {comp.name} | {comp.sport_type} | {comp.status}")
    
    print("\n3. Проверка защиты от дубликатов:")
    try:
        duplicate = Competition(
            "Чемпионат мира по футболу",
            "Футбол",
            "Москва",
            "2018-06-15",
            "2018-07-15",
            32
        )
        collection.add(duplicate)
    except ValueError as e:
        print(f"   Ошибка (корректно): {e}")
    
    print("\n4. Проверка на добавление объекта неправильного типа:")
    try:
        collection.add("Это строка, а не Competition")
    except TypeError as e:
        print(f"   Ошибка (корректно): {e}")
    
    print(f"\n5. Удаление соревнования: {competitions[0].name}")
    collection.remove(competitions[0])
    print(f"   Соревнование удалено")
    
    print(f"\n6. Повторный вывод коллекции (осталось {len(collection)} соревнований):")
    for comp in collection:
        print(f"   - {comp.name} | {comp.sport_type}")
    
    print("\n7. Добавление остальных соревнований:")
    for comp in competitions[4:]:
        collection.add(comp)
        print(f"   Добавлено: {comp.name}")
    
    print(f"\n   Итого в коллекции: {len(collection)} соревнований")
    
    return collection


def scenario_2_search_and_filter():
    """Сценарий 2: Поиск и фильтрация"""
    print_header("Сценарий 2: Поиск и фильтрация")
    
    collection = CompetitionCollection()
    competitions = create_sample_competitions()
    
    for comp in competitions:
        collection.add(comp)
    
    print("Исходная коллекция (все соревнования):")
    for comp in collection:
        print(f"   - {comp.name} | {comp.sport_type} | {comp.location} | [{comp.status}]")
    
    print("\n1. Поиск соревнования по названию 'Олимпийские игры':")
    found = collection.find_by_name("Олимпийские игры")
    if len(found) > 0:
        for comp in found:
            print(f"    Найдено: {comp.name} (ID: {comp.competition_id})")
    else:
        print(f"   Не найдено")
    
    print("\n2. Поиск соревнований по виду спорта 'Футбол':")
    football = collection.find_by_sport_type("Футбол")
    if len(football) > 0:
        for comp in football:
            print(f"    {comp.name} - {comp.location}")
    else:
        print(f"   Не найдено")
    
    print("\n3. Поиск соревнований по месту проведения 'Париж':")
    paris = collection.find_by_location("Париж")
    if len(paris) > 0:
        for comp in paris:
            print(f"   {comp.name}")
    else:
        print(f"    Не найдено")
    
    print("\n4. Фильтрация: соревнования с открытой регистрацией (get_registration):")
    registration = collection.get_registration()
    print(f"   Найдено: {len(registration)} соревнований")
    for comp in registration:
        print(f"   - {comp.name} | Статус: {comp.status}")
    
    print("\n5. Фильтрация: активные соревнования (get_active):")
    active = collection.get_active()
    print(f"   Найдено: {len(active)} соревнований")
    for comp in active:
        print(f"   - {comp.name} | Статус: {comp.status}")
    
    print("\n6. Фильтрация: соревнования с max_participants > 100:")
    large = collection.get_long_duration(100)
    print(f"   Найдено: {len(large)} соревнований")
    for comp in large:
        print(f"   - {comp.name} | Максимум участников: {comp.max_participants}")
    
    return collection


def scenario_3_sorting_and_indexing():
    """Сценарий 3: Сортировка и индексация"""
    print_header("Сценарий 3: Сортировка и индексация")
    
    collection = CompetitionCollection()
    competitions = create_sample_competitions()
    
    for comp in competitions:
        collection.add(comp)
    
    print("Исходная коллекция (порядок добавления):")
    for i, comp in enumerate(collection):
        print(f"   [{i}] {comp.name}")
    
    print("\n1. Доступ по индексу (__getitem__):")
    print(f"   collection[0]: {collection[0].name}")
    print(f"   collection[2]: {collection[2].name}")
    print(f"   collection[-1]: {collection[-1].name}")
    
    print("\n2. Срез:")
    for comp in collection[1:4]:
        print(f"   - {comp.name}")
    
    print(f"\n3. Удаление по индексу remove_at(2):")
    removed = collection.remove_at(2)
    print(f"   Удалён: {removed.name}")
    print(f"   Осталось соревнований: {len(collection)}")
    
    print("\n4. Сортировка по названию sort_by_name():")
    collection.sort_by_name()
    for i, comp in enumerate(collection):
        print(f"   {i+1}. {comp.name}")
    
    print("\n5. Сортировка по дате начала sort_by_date():")
    collection.sort_by_date()
    for i, comp in enumerate(collection):
        print(f"   {i+1}. {comp.name} - {comp.start_date}")
    
    print("\n6. Сортировка по max_participants sort_by_participants():")
    collection.sort_by_participants(reverse=True)
    for i, comp in enumerate(collection):
        print(f"   {i+1}. {comp.name} - {comp.max_participants} участников")
    
    print("\n7. Универсальная сортировка sort:")
    collection.sort(key=lambda c: c.location)
    for i, comp in enumerate(collection):
        print(f"   {i+1}. {comp.name} - {comp.location}")
    
    return collection


def main():
    """Главная функция"""
    print("=" * 70)
    print(" Лабораторная работа №2 - Коллекция соревнований")
    print("=" * 70)
    
    scenario_1_basic_operations()
    input("\n▶ Нажмите Enter для сценария 2...")
    
    scenario_2_search_and_filter()
    input("\n▶ Нажмите Enter для сценария 3...")
    
    scenario_3_sorting_and_indexing()
    
   

if __name__ == "__main__":
    main()