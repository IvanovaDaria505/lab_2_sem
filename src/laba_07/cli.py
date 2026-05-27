from typing import Optional, Callable, Union
from .models import Competition, TeamCompetition, IndividualCompetition
from .app import Application
from .exceptions import AppError, ItemNotFoundError, DuplicateItemError

class CLI:
    def __init__(self, app: Application):
        self.app = app

    def run(self) -> None:
        while True:
            self._show_menu()
            try:
                choice = int(input("Выберите пункт: "))
            except ValueError:
                print("Ошибка: введите число.")
                continue

            if choice == 0:
                print("Выход из программы. Сохраняем данные...")
                self.app.save_data()
                print("До свидания!")
                break
            elif choice == 1:
                self._add_competition()
            elif choice == 2:
                self._show_all()
            elif choice == 3:
                self._find_competition()
            elif choice == 4:
                self._delete_competition()
            elif choice == 5:
                self._filter_competitions()
            elif choice == 6:
                self._sort_competitions()
            else:
                print("Неверный пункт меню. Попробуйте снова.")

    def _show_menu(self) -> None:
        print("\n" + "=" * 50)
        print("  УПРАВЛЕНИЕ СОРЕВНОВАНИЯМИ")
        print("=" * 50)
        print("1. Добавить соревнование")
        print("2. Показать все соревнования")
        print("3. Найти соревнование")
        print("4. Удалить соревнование")
        print("5. Фильтрация и поиск")
        print("6. Сортировка")
        print("0. Выход")
        print("-" * 50)

    def _add_competition(self) -> None:
        print("\n--- ДОБАВЛЕНИЕ СОРЕВНОВАНИЯ ---")
        print("Типы: 1 - Командное, 2 - Индивидуальное")
        try:
            type_choice = int(input("Выберите тип (1/2): "))
            
            name = input("Название: ")
            sport = input("Вид спорта: ")
            location = input("Место проведения: ")
            start = input("Дата начала (ГГГГ-ММ-ДД): ")
            end = input("Дата окончания (ГГГГ-ММ-ДД): ")
            max_parts = int(input("Макс. участников: "))
            
            if type_choice == 1:
                min_teams = int(input("Мин. команд: "))
                team_size = int(input("Размер команды: "))
                comp: Competition = TeamCompetition(name, sport, location, start, end, max_parts, min_teams, team_size)
                comp.register_team("Команда А")
                comp.register_team("Команда Б")
            else:
                category = input("Категория (Профессионалы/Любители/Юниоры): ")
                prize = float(input("Призовой фонд: "))
                comp = IndividualCompetition(name, sport, location, start, end, max_parts, category, prize)
            
            self.app.add_item(comp)
            print(f"✓ Соревнование '{comp.name}' добавлено. ID: {comp.competition_id}")
        except DuplicateItemError as e:
            print(f"✗ Ошибка: {e}")
        except ValueError as e:
            print(f"✗ Ошибка ввода данных: {e}")

    def _show_all(self) -> None:
        items = self.app.get_all()
        if not items:
            print("\nКоллекция пуста.")
            return
        
        print("\n--- ВСЕ СОРЕВНОВАНИЯ ---")
        print(f"{'ID':<10} {'Название':<25} {'Вид спорта':<15} {'Статус':<15} {'Участники':<10}")
        print("-" * 75)
        for comp in items:
            parts = f"{comp.participants_count}/{comp.max_participants}"
            print(f"{comp.competition_id:<10} {comp.name[:24]:<25} {comp.sport_type:<15} {comp.status:<15} {parts:<10}")

    def _find_competition(self) -> None:
        """Поиск соревнования по ID."""
        comp_id = input("Введите ID соревнования: ")
        comp = self.app.find_by_id(comp_id)
        if comp:
            print(f"Найдено: {comp}")
            if isinstance(comp, TeamCompetition):
                print(f"  Тип: Командное | Команды: {', '.join(comp.get_teams_list())}")
            elif isinstance(comp, IndividualCompetition):
                print(f"  Тип: Индивидуальное | Категория: {comp.category} | Призовой фонд: {comp.prize_fund}")
        else:
            print(f"Соревнование с ID {comp_id} не найдено.")

    def _delete_competition(self) -> None:
        comp_id = input("Введите ID соревнования для удаления: ")
        comp = self.app.find_by_id(comp_id)
        if not comp:
            print(f"Соревнование с ID {comp_id} не найдено.")
            return
        
        confirm = input(f"Удалить '{comp.name}'? (y/n): ")
        if confirm.lower() == 'y':
            try:
                self.app.remove_item(comp_id)
                print(f"✓ Соревнование '{comp.name}' удалено.")
            except ItemNotFoundError:
                print("Ошибка: соревнование не найдено.")
        else:
            print("Удаление отменено.")

    def _filter_competitions(self) -> None:
        """Подменю фильтрации."""
        print("\n--- ФИЛЬТРАЦИЯ ---")
        print("1. По виду спорта")
        print("2. По статусу")
        print("3. По диапазону длительности")
        choice = input("Выберите тип фильтра: ")
        
        try:
            if choice == '1':
                sport = input("Введите вид спорта: ")
                result = self.app.filter_items(lambda c: c.sport_type.lower() == sport.lower())
            elif choice == '2':
                print("Статусы: Registration, In Progress, Completed")
                status = input("Введите статус: ")
                result = self.app.filter_items(lambda c: c.status.lower() == status.lower())
            elif choice == '3':
                min_days = int(input("Минимальная длительность (дней): "))
                max_days = int(input("Максимальная длительность (дней): "))
                result = self.app.filter_items(
                    lambda c: min_days <= c.get_competition_duration() <= max_days
                )
            else:
                print("Неверный выбор.")
                return
            
            if not result:
                print("Ничего не найдено по вашему запросу.")
            else:
                print(f"\nНайдено {len(result)} соревнований:")
                for comp in result:
                    print(f"  - {comp}")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")

    def _sort_competitions(self) -> None:
        """Подменю сортировки с выбором стратегии."""
        print("\n--- СОРТИРОВКА ---")
        print("Сортировать по:")
        print("1. Названию")
        print("2. Дате начала")
        print("3. Количеству участников")
        print("4. Длительности")
        choice = input("Выберите стратегию: ")
        
        key_func: Callable[[Competition], Union[str, int, float]]
        if choice == '1':
            key_func = lambda c: c.name
            desc = "названию"
        elif choice == '2':
            key_func = lambda c: c.start_date
            desc = "дате начала"
        elif choice == '3':
            key_func = lambda c: c.max_participants
            desc = "участникам"
        elif choice == '4':
            key_func = lambda c: c.get_competition_duration()
            desc = "длительности"
        else:
            print("Неверный выбор.")
            return
        
        reverse = input("Сортировать по убыванию? (y/n): ").lower() == 'y'
        sorted_items = self.app.sort_items(key=key_func, reverse=reverse)
        
        print(f"\nСортировка по {desc}:")
        for comp in sorted_items:
            print(f"  - {comp.name} ({key_func(comp)})")