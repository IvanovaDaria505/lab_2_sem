import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from container import TypedCollection, D, S
from laba_03.models import TeamCompetition, IndividualCompetition

def _add_protocol_methods():
    if not hasattr(TeamCompetition, 'display'):
        TeamCompetition.display = lambda self: (
            f"[КОМАНДНОЕ] {self.name} | {self.sport_type} | "
            f"Команд: {len(self._registered_teams)} | Статус: {self.status}"
        )
    if not hasattr(TeamCompetition, 'score'):
        TeamCompetition.score = lambda self: float(len(self._registered_teams) * 100)

    if not hasattr(IndividualCompetition, 'display'):
        IndividualCompetition.display = lambda self: (
            f"[ИНДИВИДУАЛЬНОЕ] {self.name} | {self.sport_type} | "
            f"Категория: {self.category} | Фонд: {self.prize_fund:.0f} руб. | Статус: {self.status}"
        )
    if not hasattr(IndividualCompetition, 'score'):
        IndividualCompetition.score = lambda self: self.prize_fund / 1000.0

_add_protocol_methods()

print("=" * 70)
print("СЦЕНАРИЙ 1: TypedCollection[D] — протокол Displayable")
print("=" * 70)

team = TeamCompetition("Футбол 5x5", "Футбол", "Москва",
    "2026-05-01", "2026-05-05", 20, min_teams=4, team_size=5)
team.register_team("Спартак")
team.register_team("Динамо")
team.register_team("ЦСКА")

solo = IndividualCompetition("Теннис Open", "Теннис", "Сочи",
    "2026-06-10", "2026-06-15", 32, category="Профессионалы", prize_fund=500_000)

print("\nОбъекты НЕ наследуются от Displayable явно, но имеют метод display()")
print("→ подходят под протокол.")

collection_d = TypedCollection[D]()
collection_d.add(team)
collection_d.add(solo)
print(f"Добавлено элементов: {len(collection_d)}")

print("\n>>> Вызов display() для каждого элемента:")
for i, item in enumerate(collection_d):
    print(f"  [{i}] {item.display()}")

print("\n>>> find() — поиск по условию:")
found = collection_d.find(lambda x: "Футбол" in x.display())
print(f"  Найден: {found.display() if found else 'Не найден'}")

not_found = collection_d.find(lambda x: "Хоккей" in x.display())
print(f"  Не найден: {not_found}")

print("\n>>> filter() — отбор по sport_type:")
filtered = collection_d.filter(lambda x: "Теннис" in x.display())
for item in filtered:
    print(f"  {item.display()}")

print("\n>>> map() — извлекаем имена:")
names = collection_d.map(lambda x: x.name)
print(f"  Имена: {names}")
print(f"  Тип результата: list[str]")

print("\n" + "=" * 70)
print("СЦЕНАРИЙ 2: TypedCollection[S] — протокол Scorable")
print("=" * 70)

print("\nТе же объекты, но другое ограничение — Scorable.")
print("Объекты НЕ наследуются от Scorable явно, но имеют метод score()")

collection_s = TypedCollection[S]()
collection_s.add(team)
collection_s.add(solo)
print(f"Добавлено элементов: {len(collection_s)}")

print("\n>>> Вызов score() для каждого элемента:")
for i, item in enumerate(collection_s):
    print(f"  [{i}] {item.display()} → score = {item.score():.1f}")

print("\n>>> find() — поиск по score:")
found = collection_s.find(lambda x: x.score() > 200)
print(f"  Найден (score > 200): {found.display() if found else 'Не найден'}")

print("\n>>> filter() — отбор по score:")
filtered = collection_s.filter(lambda x: x.score() < 400)
for item in filtered:
    print(f"  {item.display()} → score = {item.score():.1f}")

print("\n>>> map() — получаем удвоенные score (тип list[float]):")
doubled = collection_s.map(lambda x: x.score() * 2)
print(f"  Результат: {doubled}")
print(f"  Тип результата: list[float]")

