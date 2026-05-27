from __future__ import annotations

from typing import Optional, Callable, Union, Any

from .models import Competition, TeamCompetition, IndividualCompetition
from .app import Application
from .exceptions import AppError, ItemNotFoundError, DuplicateItemError


class CLI:

    def __init__(self, app: Application) -> None:
        self._app: Application = app

    def run(self) -> None:
        print("\n" + "=" * 72)
        print("КОНСОЛЬНОЕ ПРИЛОЖЕНИЕ ДЛЯ УПРАВЛЕНИЯ СОРЕВНОВАНИЯМИ")
        print("=" * 72)
        print(f"Автоматически загружено объектов: {len(self._app.get_all())}")

        commands = {
            1: self._add_competition,
            2: self._show_all,
            3: self._find_competition,
            4: self._delete_competition,
            5: self._filter_menu,
            6: self._sort_menu
        }

        while True:
            self._print_menu()

            choice = self._read_int("Выберите пункт: ")

            if choice == 0:
                self._exit_program()
                break

            command = commands.get(choice)

            if command is None:
                print("Ошибка: такого пункта меню нет.")
                continue

            command()

    def _print_menu(self) -> None:
        print("""
------------------------------------------------------------------------
1. Добавить соревнование
2. Показать все соревнования
3. Найти соревнование
4. Удалить соревнование
5. Фильтрация и поиск
6. Сортировка
0. Выход
------------------------------------------------------------------------
""")

    def _add_competition(self) -> None:
        print("\nДОБАВЛЕНИЕ СОРЕВНОВАНИЯ")

        print("Типы: 1 - Командное, 2 - Индивидуальное")
        type_choice = self._read_int_in_range(
            "Выберите тип (1/2): ",
            min_value=1,
            max_value=2
        )

        name = self._read_text("Название: ")
        sport = self._read_text("Вид спорта: ")
        location = self._read_text("Место проведения: ")
        start = self._read_date("Дата начала (ГГГГ-ММ-ДД): ")
        end = self._read_date("Дата окончания (ГГГГ-ММ-ДД): ")
        max_parts = self._read_positive_int("Макс. участников: ")

        try:
            if type_choice == 1:
                min_teams = self._read_positive_int("Мин. команд: ")
                team_size = self._read_positive_int("Размер команды: ")

                self._app.add_item(
                    TeamCompetition(name, sport, location, start, end, max_parts, min_teams, team_size)
                )
                print(f"✓ Командное соревнование '{name}' добавлено.")
            else:
                print("\nКатегории: Профессионалы, Любители, Юниоры")
                category = self._read_text("Категория: ")
                prize = self._read_positive_float("Призовой фонд: ")

                self._app.add_item(
                    IndividualCompetition(name, sport, location, start, end, max_parts, category, prize)
                )
                print(f"✓ Индивидуальное соревнование '{name}' добавлено.")

        except DuplicateItemError as error:
            print(f"✗ Ошибка: {error}")
        except ValueError as error:
            print(f"✗ Ошибка ввода данных: {error}")

    def _show_all(self) -> None:
        items = self._app.get_all()
        self._print_competitions(items, "ВСЕ СОРЕВНОВАНИЯ")

    def _find_competition(self) -> None:
        print("\nПОИСК СОРЕВНОВАНИЯ")

        comp_id = self._read_text("Введите ID соревнования: ")

        comp = self._app.find_by_id(comp_id)
        if comp:
            self._print_competition_details(comp)
        else:
            print(f"✗ Соревнование с ID {comp_id} не найдено.")

    def _delete_competition(self) -> None:

        print("\nУДАЛЕНИЕ СОРЕВНОВАНИЯ")

        comp_id = self._read_text("Введите ID соревнования для удаления: ")

        comp = self._app.find_by_id(comp_id)
        if not comp:
            print(f"✗ Соревнование с ID {comp_id} не найдено.")
            return

        self._print_competition_details(comp)

        confirm = self._read_bool(f"Удалить '{comp.name}'? (y/n): ")

        if confirm:
            try:
                self._app.remove_item(comp_id)
                print(f"✓ Соревнование '{comp.name}' удалено.")
            except ItemNotFoundError:
                print("✗ Ошибка: соревнование не найдено.")
        else:
            print("Удаление отменено.")

    def _filter_menu(self) -> None:
        while True:
            print("""
------------------------------------------------------------------------
ФИЛЬТРАЦИЯ
1. По виду спорта
2. По статусу
3. По диапазону длительности
0. Назад
------------------------------------------------------------------------
""")

            choice = self._read_int("Выберите тип фильтра: ")

            if choice == 0:
                return

            if choice == 1:
                self._filter_by_sport()
                return

            if choice == 2:
                self._filter_by_status()
                return

            if choice == 3:
                self._filter_by_duration()
                return

            print("Ошибка: неверный выбор.")

    def _filter_by_sport(self) -> None:
        print("\nФильтр по виду спорта")

        sport = self._read_text("Введите вид спорта: ")

        result = self._app.filter_items(
            lambda c: c.sport_type.lower() == sport.lower()
        )
        self._print_competitions(
            result,
            f"СОРЕВНОВАНИЯ ПО ВИДУ СПОРТА: {sport.upper()}"
        )

    def _filter_by_status(self) -> None:
        print("\nФильтр по статусу")
        print("Статусы: Registration, In Progress, Completed")

        status = self._read_text("Введите статус: ")

        result = self._app.filter_items(
            lambda c: c.status.lower() == status.lower()
        )
        self._print_competitions(
            result,
            f"СОРЕВНОВАНИЯ СО СТАТУСОМ: {status.upper()}"
        )

    def _filter_by_duration(self) -> None:
        print("\nФильтр по длительности")

        min_days = self._read_positive_int("Минимальная длительность (дней): ")
        max_days = self._read_positive_int("Максимальная длительность (дней): ")

        try:
            result = self._app.filter_items(
                lambda c: min_days <= c.get_competition_duration() <= max_days
            )
            self._print_competitions(
                result,
                f"СОРЕВНОВАНИЯ ДЛИТЕЛЬНОСТЬЮ ОТ {min_days} ДО {max_days} ДНЕЙ"
            )
        except ValueError as error:
            print(f"✗ Ошибка: {error}")

    def _sort_menu(self) -> None:
        while True:
            print("""
------------------------------------------------------------------------
СОРТИРОВКА
1. По названию
2. По дате начала
3. По количеству участников
4. По длительности
0. Назад
------------------------------------------------------------------------
""")

            choice = self._read_int("Выберите стратегию сортировки: ")

            if choice == 0:
                return

            if choice in (1, 2, 3, 4):
                reverse = self._read_bool("Сортировать по убыванию? (y/n): ")
                self._perform_sort(choice, reverse)
                return

            print("Ошибка: неверный выбор.")

    def _perform_sort(self, choice: int, reverse: bool) -> None:
        key_func: Callable[[Competition], Any]
        desc: str

        if choice == 1:
            key_func = lambda c: c.name
            desc = "названию"
        elif choice == 2:
            key_func = lambda c: c.start_date
            desc = "дате начала"
        elif choice == 3:
            key_func = lambda c: c.max_participants
            desc = "количеству участников"
        elif choice == 4:
            key_func = lambda c: c.get_competition_duration()
            desc = "длительности"
        else:
            return

        sorted_items = self._app.sort_items(key=key_func, reverse=reverse)
        
        direction = "по убыванию" if reverse else "по возрастанию"
        self._print_competitions(
            sorted_items,
            f"СОРТИРОВКА ПО {desc.upper()} ({direction})",
            show_key=key_func
        )

    def _exit_program(self) -> None:
        print("Выход из программы. Сохраняем данные...")
        try:
            self._app.save_data()
            print("До свидания!")

        except AppError as error:
            print(f"✗ Ошибка сохранения: {error}")
            print("Программа завершена без сохранения.")

    def _print_competitions(
        self,
        competitions: list[Competition],
        title: str,
        show_key: Callable[[Competition], Any] | None = None
    ) -> None:
        print(f"\n{title}")

        if not competitions:
            print("Список пуст.")
            return

        print("-" * 90)
        header = (
            f"{'ID':<10}"
            f"{'Название':<25}"
            f"{'Вид спорта':<15}"
            f"{'Статус':<15}"
            f"{'Участники':<12}"
        )
        
        if show_key:
            header += f"{'Значение':<13}"
        
        print(header)
        print("-" * 90)

        for comp in competitions:
            parts = f"{comp.participants_count}/{comp.max_participants}"
            row = (
                f"{comp.competition_id:<10}"
                f"{comp.name[:24]:<25}"
                f"{comp.sport_type:<15}"
                f"{comp.status:<15}"
                f"{parts:<12}"
            )
            
            if show_key:
                row += f"{str(show_key(comp)):<13}"
            
            print(row)

        print("-" * 90)

    def _print_competition_details(self, comp: Competition) -> None:
        print("\n" + "=" * 50)
        print(f"ИНФОРМАЦИЯ О СОРЕВНОВАНИИ")
        print("=" * 50)
        print(f"Найдено: {comp}")
        if isinstance(comp, TeamCompetition):
            print(f"  Тип: Командное | Команды: {', '.join(comp.get_teams_list())}")
        elif isinstance(comp, IndividualCompetition):
            print(f"  Тип: Индивидуальное | Категория: {comp.category} | Призовой фонд: {comp.prize_fund}")
        print("=" * 50)

    def _read_text(self, prompt: str) -> str:
        while True:
            raw_value = input(prompt).strip()

            if raw_value:
                return raw_value

            print("Ошибка: строка не может быть пустой.")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw_value = input(prompt).strip()

            try:
                return int(raw_value)

            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_int_in_range(self, prompt: str, min_value: int, max_value: int) -> int:
        while True:
            raw_value = input(prompt).strip()

            try:
                value = int(raw_value)

            except ValueError:
                print("Ошибка: введите целое число.")
                continue

            if value < min_value or value > max_value:
                print(f"Ошибка: значение должно быть от {min_value} до {max_value}.")
                continue

            return value

    def _read_positive_int(self, prompt: str) -> int:
        while True:
            raw_value = input(prompt).strip()

            try:
                value = int(raw_value)

            except ValueError:
                print("Ошибка: введите целое число.")
                continue

            if value <= 0:
                print("Ошибка: значение должно быть больше 0.")
                continue

            return value

    def _read_positive_float(self, prompt: str) -> float:
        while True:
            raw_value = input(prompt).strip().replace(",", ".")

            try:
                value = float(raw_value)

            except ValueError:
                print("Ошибка: введите число.")
                continue

            if value <= 0:
                print("Ошибка: значение должно быть больше 0.")
                continue

            return value

    def _read_date(self, prompt: str) -> str:
        while True:
            raw_value = input(prompt).strip()

            if not raw_value:
                print("Ошибка: дата не может быть пустой.")
                continue

            parts = raw_value.split("-")
            if len(parts) != 3:
                print("Ошибка: неверный формат. Используйте ГГГГ-ММ-ДД.")
                continue

            try:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    print("Ошибка: неверная дата.")
                    continue
            except ValueError:
                print("Ошибка: неверный формат. Используйте ГГГГ-ММ-ДД.")
                continue

            return raw_value

    def _read_bool(self, prompt: str) -> bool:
        while True:
            raw_value = input(prompt).strip().lower()

            if raw_value in {"y", "yes", "д", "да", "1"}:
                return True

            if raw_value in {"n", "no", "н", "нет"}:
                return False

            print("Ошибка: введите y/n или да/нет.")