import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'laba_03'))
sys.path.insert(0, os.path.dirname(__file__))

from models import TeamCompetition, IndividualCompetition, CompetitionCollection
from interfaces import Printable, Comparable



def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_all(items: list):
    for item in items:
        if isinstance(item, Printable):
            print(f"  {item.to_string()}")

def scenario_1_interfaces_and_universal_function():
    print_section("СЦЕНАРИЙ 1: Интерфейс как тип, универсальная функция, isinstance")
    
    team = TeamCompetition(
        name="Кубок Чемпионов",
        sport_type="Футбол",
        location="Барселона",
        start_date="2025-06-01",
        end_date="2025-06-15",
        max_participants=200,
        min_teams=4,
        team_size=25
    )
    
    individual = IndividualCompetition(
        name="Гран-при по теннису",
        sport_type="Теннис",
        location="Париж",
        start_date="2025-07-01",
        end_date="2025-07-10",
        max_participants=64,
        category="Профессионалы",
        prize_fund=1000000.0
    )
    
    team.register_team("Спартак")
    team.register_team("ЦСКА")
    
    print("\n1. Проверка isinstance:")
    print(f"   team является Printable? {isinstance(team, Printable)}")
    print(f"   team является Comparable? {isinstance(team, Comparable)}")
    print(f"   individual является Printable? {isinstance(individual, Printable)}")
    print(f"   individual является Comparable? {isinstance(individual, Comparable)}")
    
    print("\n2. Вызов интерфейсного метода to_string() напрямую:")
    print(f"   {team.to_string()}")
    print(f"   {individual.to_string()}")
    
    print("\n3. Универсальная функция print_all() с интерфейсом как типом:")
    items = [team, individual]
    print_all(items)

def scenario_2_collection_filter_by_interface():
    print_section("СЦЕНАРИЙ 2: колеекция, фильтрация по интерфейсу, полиморфизм")
    
    collection = CompetitionCollection()
    
    team1 = TeamCompetition("Чемпионат по футболу", "Футбол", "Лондон", "2025-05-01", "2025-05-15", 200, 8, 25)
    team2 = TeamCompetition("Кубок по баскетболу", "Баскетбол", "Афины", "2025-06-01", "2025-06-10", 120, 6, 12)
    ind1 = IndividualCompetition("Открытый чемпионат", "Теннис", "Нью-Йорк", "2025-07-01", "2025-07-14", 128, "Профессионалы", 2000000.0)
    ind2 = IndividualCompetition("Юниорский турнир", "Плавание", "Токио", "2025-08-01", "2025-08-05", 500, "Юниоры", 300000.0)
    
    collection.add(team1)
    collection.add(team2)
    collection.add(ind1)
    collection.add(ind2)
    
    team1.register_team("Реал Мадрид")
    team1.register_team("Барселона")
    team2.register_team("Панатинаикос")
    
    print("\n1. Единый список объектов разных типов:")
    for comp in collection:
        print(f"   - {type(comp).__name__}: {comp.name}")
    
    print("\n2. Фильтрация коллекции — get_printable():")
    printable_items = collection.get_printable()
    print(f"   Найдено объектов с интерфейсом Printable: {len(printable_items)}")
    print_all(printable_items)
    
    print("\n3. Фильтрация коллекции — get_comparable():")
    comparable_items = collection.get_comparable()
    print(f"   Найдено объектов с интерфейсом Comparable: {len(comparable_items)}")
    for comp in comparable_items:
        print(f"   - {comp.to_string()}")
    
    print("\n4. Полиморфный вызов to_string() без проверок типа:")
    for comp in collection:
        print(f"   {comp.to_string()}")

def scenario_3_sorting_and_compare():
    print_section("СЦЕНАРИЙ 3: сортировка через combarable, сравнение объектов")
    
    ind1 = IndividualCompetition("Турнир Мастерс", "Гольф", "Огаста", "2025-04-01", "2025-04-07", 90, "Мастера", 5000000.0)
    ind2 = IndividualCompetition("Открытый чемпионат", "Гольф", "Сент-Эндрюс", "2025-07-01", "2025-07-05", 156, "Профессионалы", 1500000.0)
    ind3 = IndividualCompetition("Кубок Вызова", "Гольф", "Дубай", "2025-11-01", "2025-11-04", 60, "Любители", 300000.0)
    
    print("\n1. Сравнение объектов через compare_to() по призовому фонду:")
    result = ind1.compare_to(ind2)
    print(f"   {ind1.name} (5M) vs {ind2.name} (1.5M): {result} (ожидалось > 0)")
    
    result = ind2.compare_to(ind3)
    print(f"   {ind2.name} (1.5M) vs {ind3.name} (300K): {result} (ожидалось > 0)")
    
    result = ind3.compare_to(ind1)
    print(f"   {ind3.name} (300K) vs {ind1.name} (5M): {result} (ожидалось < 0)")
    
    print("\n2. Архитектурное поведение — сортировка через интерфейс Comparable:")
    collection = CompetitionCollection()
    collection.add(ind1)
    collection.add(ind2)
    collection.add(ind3)
    
    comparable_items = collection.get_comparable()
    
    # Сортировка пузырьком через compare_to (без условий isinstance)
    n = len(comparable_items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if comparable_items[j].compare_to(comparable_items[j + 1]) > 0:
                comparable_items[j], comparable_items[j + 1] = comparable_items[j + 1], comparable_items[j]
    
    print("   Сортировка по возрастанию призового фонда:")
    for i, comp in enumerate(comparable_items, 1):
        print(f"   {i}. {comp.to_string()}")
    
    print("\n3. Показать, что объекты реализуют несколько интерфейсов:")
    for comp in [ind1, ind2, ind3]:
        is_printable = isinstance(comp, Printable)
        is_comparable = isinstance(comp, Comparable)
        print(f"   {comp.name}: Printable={is_printable}, Comparable={is_comparable}")

def main():
    print("\n" + "=" * 60)
    print(" " * 15 + "Лабораторная работа №4")
    print(" " * 10 + "Интерфейсы и абстрактные классы")
    print("=" * 60)
    
    scenario_1_interfaces_and_universal_function()
    input("\nНажмите Enter для перехода к Сценарию 2...")
    
    scenario_2_collection_filter_by_interface()
    input("\nНажмите Enter для перехода к Сценарию 3...")
    
    scenario_3_sorting_and_compare()
    
    print("\n" + "=" * 60)
    print("=" * 60)

if __name__ == "__main__":
    main()