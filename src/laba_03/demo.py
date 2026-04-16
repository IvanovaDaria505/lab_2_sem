from models import TeamCompetition, IndividualCompetition, CompetitionCollection
from base import Competition
def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def scenario_1_inheritance_and_polymorphism():
    print_section("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")
    
    team_comp = TeamCompetition(
        name="Кубок Европы",
        sport_type="Футбол",
        location="Мадрид",
        start_date="2025-06-10",
        end_date="2025-07-10",
        max_participants=230,
        min_teams=4,
        team_size=23
    )
    
    ind_comp = IndividualCompetition(
        name="Турнир",
        sport_type="Теннис",
        location="Лондон",
        start_date="2025-07-01",
        end_date="2025-07-14",
        max_participants=128,
        category="Профессионалы",
        prize_fund=500000.0
    )
    
    print("\n1. Созданы объекты разных классов. Проверка типов (isinstance):")
    print(f"   team_comp является TeamCompetition? {isinstance(team_comp, TeamCompetition)}")
    print(f"   team_comp является Competition? {isinstance(team_comp, Competition)}")
    print(f"   ind_comp является IndividualCompetition? {isinstance(ind_comp, IndividualCompetition)}")
    print(f"   ind_comp является TeamCompetition? {isinstance(ind_comp, TeamCompetition)}")
    
    print("\n2. Демонстрация использования super() в __init__:")
    print(f"   Базовые атрибуты team_comp: ID={team_comp.competition_id}, Статус={team_comp.status}")
    print(f"   Базовые атрибуты ind_comp: ID={ind_comp.competition_id}, Статус={ind_comp.status}")
    
    print("\n3. Вызов методов дочерних классов:")
    team_comp.register_team("Спартак")
    team_comp.register_team("Реал Мадрид")
    team_comp.register_team("Бавария")
    team_comp.register_team("Манчестер Сити")
    print(f"   Зарегистрированные команды: {team_comp.get_teams_list()}")
    
    ind_comp.set_rating_requirement(1500)
    print(f"   Требования к рейтингу для тенниса: {ind_comp.get_rating_requirement()}")
    
    print("\n4. Переопределенный метод __str__():")
    print(team_comp)
    print(ind_comp)
    
    print("\n5. Полиморфизм метода calculate_organizer_fee():")
    print(f"   Взнос за командное соревнование: {team_comp.calculate_organizer_fee():.2f} руб.")
    print(f"   Взнос за индивидуальное соревнование: {ind_comp.calculate_organizer_fee():.2f} руб.")

def scenario_2_collection_integration():
    print_section("СЦЕНАРИЙ 2: ИНТЕГРАЦИЯ С КОЛЛЕКЦИЕЙ И ФИЛЬТРАЦИЯ")
    
    collection = CompetitionCollection()
    
    comps = [
        TeamCompetition("Чемпионат Мира по хоккею", "Хоккей", "Прага", "2025-05-01", "2025-05-20", 250, 8, 25),
        IndividualCompetition("Марафон в Берлине", "Бег", "Берлин", "2025-09-25", "2025-09-25", 40000, "Любители", 100000.0),
        TeamCompetition("Лига Чемпионов по волейболу", "Волейбол", "Рим", "2025-11-10", "2025-11-20", 144, 6, 12),
        IndividualCompetition("Чемпионат по плаванию", "Плавание", "Барселона", "2025-08-01", "2025-08-05", 500, "Юниоры", 50000.0),
    ]
    
    print("\n1. Добавление объектов разных классов в одну коллекцию:")
    for comp in comps:
        collection.add(comp)
        print(f"   Добавлено: {comp.name} (Тип: {type(comp).__name__})")
    
    print(f"\n2. Всего элементов в коллекции: {len(collection)}")
    
    print("\n3. Единый интерфейс вызова полиморфного метода для всех объектов:")
    total_fee = 0
    for comp in collection:
        fee = comp.calculate_organizer_fee()
        total_fee += fee
        print(f"   {comp.name:<35} -> Взнос: {fee:>8.2f} руб.")
    print(f"   {' ' * 35}    ИТОГО: {total_fee:>8.2f} руб.")
    
    print("\n4. Демонстрация фильтрации по типу (get_only_team_competitions):")
    team_coll = collection.filter_by_type(TeamCompetition)
    print(f"   Найдено командных соревнований: {len(team_coll)}")
    for comp in team_coll:
        print(f"   - {comp.name} (Команд: {len(comp.get_teams_list())})")
        
    print("\n5. Демонстрация фильтрации по типу (get_only_individual_competitions):")
    ind_coll = collection.filter_by_type(IndividualCompetition)
    print(f"   Найдено индивидуальных соревнований: {len(ind_coll)}")
    for comp in ind_coll:
        print(f"   - {comp.name} (Категория: {comp.category})")

def scenario_3_polymorphic_behavior():
    print_section("СЦЕНАРИЙ 3: ПОЛИМОРФНОЕ ПОВЕДЕНИЕ БЕЗ УСЛОВИЙ")
    
    t1 = TeamCompetition("Региональный турнир", "Баскетбол", "Самара", "2025-04-10", "2025-04-15", 60, 4, 12)
    t2 = IndividualCompetition("Открытый кубок", "Бадминтон", "Казань", "2025-04-20", "2025-04-22", 64, "Мастера", 200000.0)
    
    print("\n1. Подготовка соревнований:")
    t1.register_team("ЦСКА")
    t1.register_team("Химки")
    t1.register_team("Зенит")
    t1.register_team("Локомотив")
    
    for i in range(1, 17):
        t2._participants.append(f"Игрок_{i}")
    
    print(f"   В командном турнире заявлено команд: {len(t1.get_teams_list())}")
    print(f"   В индивидуальном турнире участников: {t2.participants_count}")
    
    print("\n2. Единый вызов next_status() для разных объектов:")
    print("   Запуск командного турнира:")
    print(f"   {t1.next_status()}")
    print("   Запуск индивидуального турнира:")
    print(f"   {t2.next_status()}")
    
    print(f"\n   Статус t1: {t1.status}")
    print(f"   Статус t2: {t2.status}")
    
    print("\n3. Демонстрация единого вызова calculate_organizer_fee():")
    competitions = [t1, t2]
    for comp in competitions:
        fee = comp.calculate_organizer_fee()
        print(f"   {type(comp).__name__:<22} (Статус: {comp.status:<12}) -> Взнос: {fee:.2f} руб.")
    
    print("\n4. Проверка разных результатов __str__ через общий вызов print:")
    for comp in competitions:
        print(comp)

def main():
    print("\n" + "=" * 60)
    print(" " * 15 + "ЛАБОРАТОРНАЯ РАБОТА №3")
    print("=" * 60)
    
    scenario_1_inheritance_and_polymorphism()
    input("\nНажмите Enter для перехода к Сценарию 2...")
    
    scenario_2_collection_integration()
    input("\nНажмите Enter для перехода к Сценарию 3...")
    
    scenario_3_polymorphic_behavior()
    
    print("\n" + "=" * 60)
    print("=" * 60)

if __name__ == "__main__":
    main()