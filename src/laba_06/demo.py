"""
Демонстрационный модуль для лабораторной работы №6
"""

import sys
import os
from typing import Optional, List

# Настраиваем пути
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)

# ВАЖНО: порядок имеет значение!
sys.path.insert(0, src_dir)  # Чтобы laba_03 мог импортировать laba_03.base
sys.path.insert(0, os.path.join(src_dir, 'laba_01'))  # Чтобы model.py нашёл validate
sys.path.insert(0, os.path.join(src_dir, 'laba_03'))  # Чтобы models.py был доступен

# Теперь все импорты работают
from model import Competition as CompetitionV1
from models import TeamCompetition, IndividualCompetition

# Импорт из текущей папки
from container import TypedCollection, Displayable, Scorable


def print_section(title: str) -> None:
    """Вывод заголовка раздела"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_task_3_basic_typed_collection() -> None:
    """Демонстрация задания на 3: все методы из ЛР-2"""
    print_section("ЗАДАНИЕ НА 3: ТИПИЗИРОВАННАЯ КОЛЛЕКЦИЯ (ВСЕ МЕТОДЫ ИЗ ЛР-2)")
    
    collection: TypedCollection[CompetitionV1] = TypedCollection()
    
    comps = [
        CompetitionV1("Чемпионат мира по футболу", "Футбол", "Москва", "2024-06-15", "2024-07-15", 32),
        CompetitionV1("Олимпийские игры", "Биатлон", "Париж", "2024-07-26", "2024-08-11", 10000),
        CompetitionV1("Турнир по теннису", "Теннис", "Лондон", "2024-08-01", "2024-08-15", 128),
        CompetitionV1("Кубок Европы по футболу", "Футбол", "Берлин", "2024-09-01", "2024-09-30", 24),
        CompetitionV1("Марафон", "Бег", "Бостон", "2024-10-01", "2024-10-01", 30000),
    ]
    
    print("\n1. Добавление элементов:")
    for comp in comps:
        collection.add(comp)
        print(f"   ✓ {comp.name}")
    
    print(f"\n   Всего: {len(collection)} элементов")
    
    # Проверка дубликатов
    print("\n2. Проверка дубликатов:")
    try:
        collection.add(comps[0])
    except ValueError as e:
        print(f"   ✗ {e}")
    
    # find_by_name
    print("\n3. Поиск по названию:")
    result = collection.find_by_name("Олимпийские игры")
    for comp in result:
        print(f"   ✓ {comp.name}")
    
    # find_by_sport_type
    print("\n4. Поиск по виду спорта:")
    result = collection.find_by_sport_type("Футбол")
    for comp in result:
        print(f"   ✓ {comp.name}")
    
    # find_by_location
    print("\n5. Поиск по локации:")
    result = collection.find_by_location("Москва")
    for comp in result:
        print(f"   ✓ {comp.name}")
    
    # Фильтрация по статусу
    print("\n6. Фильтрация по статусу:")
    print(f"   Активных: {len(collection.get_active())}")
    print(f"   На регистрации: {len(collection.get_registration())}")
    print(f"   Завершенных: {len(collection.get_completed())}")
    
    # get_long_duration
    print("\n7. Соревнования с >100 участников:")
    result = collection.get_long_duration(100)
    for comp in result:
        print(f"   ✓ {comp.name}: {comp.max_participants} уч.")
    
    # Сортировки
    print("\n8. Сортировка по названию:")
    collection.sort_by_name()
    for comp in collection:
        print(f"   - {comp.name}")
    
    print("\n9. Сортировка по длительности:")
    collection.sort_by_duration(reverse=True)
    for comp in collection:
        print(f"   - {comp.name}: {comp.get_competition_duration()} дн.")
    
    # Индексация
    print("\n10. Индексация:")
    print(f"   [0]: {collection[0].name}")
    print(f"   [-1]: {collection[-1].name}")
    
    # Срез
    print("\n11. Срез [1:3]:")
    for comp in collection[1:3]:
        print(f"   - {comp.name}")
    
    # remove_at
    print("\n12. Удаление по индексу:")
    removed = collection.remove_at(1)
    print(f"   Удален: {removed.name}, осталось: {len(collection)}")
    
    # Валидация типов
    print("\n13. Валидация типов:")
    print("   ✓ mypy проверит несоответствие типов")


def demo_task_4_extended_methods() -> None:
    """Демонстрация задания на 4: find, filter, map"""
    print_section("ЗАДАНИЕ НА 4: find, filter, map")
    
    collection: TypedCollection[CompetitionV1] = TypedCollection()
    
    comps = [
        CompetitionV1("Чемпионат мира", "Футбол", "Москва", "2024-06-15", "2024-07-15", 32),
        CompetitionV1("Олимпийские игры", "Биатлон", "Париж", "2024-07-26", "2024-08-11", 10000),
        CompetitionV1("Турнир по теннису", "Теннис", "Лондон", "2024-08-01", "2024-08-15", 128),
        CompetitionV1("Кубок Европы", "Футбол", "Берлин", "2024-09-01", "2024-09-30", 24),
        CompetitionV1("Марафон", "Бег", "Бостон", "2024-10-01", "2024-10-01", 30000),
    ]
    
    for comp in comps:
        collection.add(comp)
    
    # find() - успех
    print("\n1. find() - поиск футбола:")
    found = collection.find(lambda c: c.sport_type == "Футбол")
    print(f"   ✓ Найдено: {found.name}" if found else "   ✗ Не найдено")
    
    # find() - None
    print("\n2. find() - несуществующий:")
    found = collection.find(lambda c: c.max_participants > 50000)
    print(f"   Результат: {found} (None)")
    
    # filter()
    print("\n3. filter() - длительность > 10 дней:")
    result = collection.filter(lambda c: c.get_competition_duration() > 10)
    for comp in result:
        print(f"   ✓ {comp.name}: {comp.get_competition_duration()} дн.")
    
    # map() -> list[str]
    print("\n4. map() -> list[str] (имена):")
    names: List[str] = collection.map(lambda c: c.name)
    print(f"   Тип: {type(names).__name__}[{type(names[0]).__name__}]")
    for name in names:
        print(f"   - {name}")
    
    # map() -> list[float]
    print("\n5. map() -> list[float] (длительности):")
    durations: List[float] = collection.map(lambda c: float(c.get_competition_duration()))
    print(f"   Тип: {type(durations).__name__}[{type(durations[0]).__name__}]")
    for name, dur in zip(names, durations):
        print(f"   - {name}: {dur} дн.")
    
    print("\n   ✓ map() меняет тип: str → float → tuple")


def demo_task_5_protocols() -> None:
    """Демонстрация задания на 5: протоколы"""
    print_section("ЗАДАНИЕ НА 5: ПРОТОКОЛЫ")
    
    # Monkey-patching (только для демонстрации!)
    TeamCompetition.display = lambda self: f"[Командное] {self.name} | {self.sport_type}"
    IndividualCompetition.display = lambda self: f"[Индивидуальное] {self.name} | {self.sport_type} | Категория: {self.category}"
    TeamCompetition.score = lambda self: float(len(self._registered_teams) * 25.0 if hasattr(self, '_registered_teams') else 0)
    IndividualCompetition.score = lambda self: float(self.prize_fund / 1000.0)
    
    # Сценарий 1: Displayable
    print("\nСЦЕНАРИЙ 1: TypedCollection[D] (Displayable)")
    print("-" * 60)
    
    collection_d: TypedCollection[D] = TypedCollection()
    
    team = TeamCompetition("Кубок Европы", "Футбол", "Мадрид", "2025-06-10", "2025-07-10", 230, 4, 23)
    ind = IndividualCompetition("Турнир по теннису", "Теннис", "Лондон", "2025-07-01", "2025-07-14", 128, "Профессионалы", 500000.0)
    
    # Регистрируем команды
    for team_name in ["Спартак", "Реал", "Барселона", "Бавария"]:
        team.register_team(team_name)
    
    collection_d.add(team)
    collection_d.add(ind)
    
    print("Объекты НЕ наследуются от Displayable, но имеют метод display():")
    for item in collection_d:
        print(f"  {item.display()}")
    
    # Сценарий 2: Scorable
    print("\nСЦЕНАРИЙ 2: TypedCollection[S] (Scorable)")
    print("-" * 60)
    
    collection_s: TypedCollection[S] = TypedCollection()
    
    team2 = TeamCompetition("Лига Чемпионов", "Волейбол", "Рим", "2025-11-10", "2025-11-20", 144, 6, 12)
    ind2 = IndividualCompetition("Чемпионат по плаванию", "Плавание", "Барселона", "2025-08-01", "2025-08-05", 500, "Юниоры", 50000.0)
    
    for t in ["ЦСКА", "Зенит", "Локомотив", "Динамо", "Спартак", "Краснодар"]:
        team2.register_team(t)
    
    collection_s.add(team2)
    collection_s.add(ind2)
    
    print("Вызов score() для каждого объекта:")
    for item in collection_s:
        print(f"  {item.score():.1f} баллов - {item.name}")
    
    avg = collection_s.calculate_average_score()
    print(f"\n  Средний балл: {avg:.1f}")


def main() -> None:
    """Главная функция"""
    print("\n" + "=" * 70)
    print("  ЛАБОРАТОРНАЯ РАБОТА №6: Generics и typing")
    print("=" * 70)
    
    demo_task_3_basic_typed_collection()
    input("\n▶ Enter для задания 4...")
    
    demo_task_4_extended_methods()
    input("\n▶ Enter для задания 5...")
    
    demo_task_5_protocols()
    
    print("\n" + "=" * 70)
    print("  ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)


if __name__ == "__main__":
    main()