import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'laba_03'))
from models import TeamCompetition, IndividualCompetition
from base import Competition
from laba_05.collection import CompetitionCollection
from laba_05 import strategies as strat

def create_sample_collection():
    collection = CompetitionCollection()
    
    collection.add(IndividualCompetition(
        "Быстрая ракетка", "Теннис", "Москва",
        "2026-06-01", "2026-06-02", 32, "Профессионалы", 50000.0
    ))
    collection.add(IndividualCompetition(
        "Зимний спринт", "Лыжи", "Сочи",
        "2026-07-10", "2026-07-15", 50, "Любители", 25000.0
    ))
    collection.add(IndividualCompetition(
        "Кубок Мечты", "Футбол", "Санкт-Петербург",
        "2026-08-01", "2026-08-05", 100, "Юниоры", 100000.0
    ))
    
    collection.add(TeamCompetition(
        "Городская Лига", "Баскетбол", "Казань",
        "2026-09-01", "2026-09-03", 60, 4, 5
    ))
    collection.add(TeamCompetition(
        "Эстафета Чемпионов", "Плавание", "Калининград",
        "2026-05-20", "2026-05-21", 30, 3, 4
    ))
    collection.add(TeamCompetition(
        "Весенний Кубок", "Волейбол", "Екатеринбург",
        "2026-10-10", "2026-10-15", 80, 6, 6
    ))
    collection.add(TeamCompetition(
        "Ледовая Битва", "Хоккей", "Омск",
        "2026-11-01", "2026-11-03", 40, 4, 5
    ))
    
    for comp in collection.get_all():
        if isinstance(comp, TeamCompetition):
            comp.register_team(f"Team_{comp.name[:3]}_A")
            comp.register_team(f"Team_{comp.name[:3]}_B")
    
    return collection

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_collection(collection, description=""):
    print(f"\n{description} (Элементов: {len(collection)})")
    for item in collection:
        print(f"  - {item.name} | {item.sport_type} | Статус: {item.status} | Макс. участников: {item.max_participants}")

def scenario_1():
    print_section("СЦЕНАРИЙ 1: Цепочка filter -> sort -> apply")
    
    collection = create_sample_collection()
    print_collection(collection, "Исходная коллекция:")
    
    print("\n--- Шаг 1. filter_by(is_long_duration) ---")
    long_events = collection.filter_by(strat.is_long_duration)
    print_collection(long_events, "Только длительные соревнования:")
    
    print("\n--- Шаг 2. sort_by(by_name) ---")
    sorted_events = long_events.sort_by(strat.by_name)
    print_collection(sorted_events, "Отсортировано по названию:")
    
    print("\n--- Шаг 3. apply(StatusUpgradeStrategy) ---")
    sorted_events.apply(strat.StatusUpgradeStrategy())
    print_collection(sorted_events, "Статусы изменены (Registration -> In Progress):")
    
    print("\n--- Полная цепочка для исходной коллекции ---")
    collection2 = create_sample_collection()
    result = (collection2
              .filter_by(strat.is_team_competition)
              .sort_by(strat.by_max_participants)
              .apply(strat.StatusUpgradeStrategy()))
    print_collection(result, "Результат: командные, сортировка по участникам, статус изменен:")

def scenario_2():
    print_section("СЦЕНАРИЙ 2: Замена стратегии")
    
    collection = create_sample_collection()
    
    print("\n--- Стратегия сортировки A: по длительности ---")
    result_a = CompetitionCollection(collection.get_all()).sort_by(strat.by_duration)
    for item in result_a:
        print(f"  - {item.name}: Длительность = {item.get_competition_duration()} дн.")
    
    print("\n--- Стратегия сортировки B: по статусу -> названию ---")
    for comp in collection.get_all():
        if "Быстрая" in comp.name or "Зимний" in comp.name:
            comp.next_status()
    
    result_b = CompetitionCollection(collection.get_all()).sort_by(strat.by_status_and_name)
    for item in result_b:
        print(f"  - {item.name}: Статус = {item.status}")
    
    print("\n--- Сравнение: lambda vs именованная функция ---")
    collection3 = create_sample_collection()
    filtered_named = collection3.filter_by(strat.is_team_competition)
    print(f"Именованная is_team_competition: {len(filtered_named)} соревнований")
    filtered_lambda = collection3.filter_by(lambda c: isinstance(c, TeamCompetition))
    print(f"Lambda-выражение: {len(filtered_lambda)} соревнований")
    print("Результат идентичен! Lambda удобен для одноразовых простых условий.")

def scenario_3():
    print_section("СЦЕНАРИЙ 3: Callable-объекты (паттерн Стратегия)")
    
    collection = create_sample_collection()
    print_collection(collection, "Исходная коллекция для теста стратегий:")
    
    print("\n--- Применяем FeeCalculationStrategy ---")
    fee_strategy = strat.FeeCalculationStrategy()
    print("Отчет по взносам (без изменения объектов):")
    for comp in collection:
        result = fee_strategy(comp)
        print(f"  {result}")
    
    print("\n--- Применяем RegistrationMultiplierStrategy ---")
    reg_multiplier = strat.RegistrationMultiplierStrategy()
    collection.apply(reg_multiplier)
    print_collection(collection, "Лимиты участников удвоены (стратегия применена):")
    
    print("\n--- Взаимозаменяемость стратегий ---")
    collection.apply(lambda c: (setattr(c, '_location', c.location.upper()) or c))
    print("Применили lambda-стратегию: все локации в верхнем регистре.")
    for item in collection:
        print(f"  - {item.name}: {item.location}") 

if __name__ == "__main__":
    scenario_1()
    scenario_2()
    scenario_3()