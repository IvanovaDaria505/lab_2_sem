from __future__ import annotations

from typing import Callable, Any

from .models import (
    Competition,
    TeamCompetition,
    IndividualCompetition
)

from .app import Application

from .exceptions import (
    AppError,
    ItemNotFoundError,
    DuplicateItemError,
    StorageError
)


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
5. Фильтрация
6. Сортировка
0. Выход
------------------------------------------------------------------------
""")

    def _add_competition(self) -> None:
        
        print("\nДОБАВЛЕНИЕ СОРЕВНОВАНИЯ")

        print("1. Командное")
        print("2. Индивидуальное")

        type_choice = self._read_int_in_range(
            "Выберите тип: ",
            1,
            2
        )

        name = self._read_text("Название: ")
        sport = self._read_text("Вид спорта: ")
        location = self._read_text("Место проведения: ")

        start_date = self._read_date(
            "Дата начала (ГГГГ-ММ-ДД): "
        )

        end_date = self._read_date(
            "Дата окончания (ГГГГ-ММ-ДД): "
        )

        max_participants = self._read_positive_int(
            "Максимум участников: "
        )

        try:
            if type_choice == 1:
                min_teams = self._read_positive_int(
                    "Минимум команд: "
                )

                team_size = self._read_positive_int(
                    "Размер команды: "
                )

                self._app.add_item(
                    TeamCompetition(
                        name,
                        sport,
                        location,
                        start_date,
                        end_date,
                        max_participants,
                        min_teams,
                        team_size
                    )
                )

            else:
                category = self._read_text(
                    "Категория: "
                )

                prize_fund = self._read_positive_float(
                    "Призовой фонд: "
                )

                self._app.add_item(
                    IndividualCompetition(
                        name,
                        sport,
                        location,
                        start_date,
                        end_date,
                        max_participants,
                        category,
                        prize_fund
                    )
                )

            print("Соревнование успешно добавлено.")

        except (
            DuplicateItemError,
            ValueError,
            TypeError
        ) as error:
            print(f"Ошибка: {error}")

    def _show_all(self) -> None:
      
        competitions = self._app.get_all()

        self._print_competitions(
            competitions,
            "Все соревнования"
        )

    def _find_competition(self) -> None:
        
        print("\nПОИСК СОРЕВНОВАНИЯ")

        competition_id = self._read_text(
            "Введите ID соревнования: "
        )

        competition = self._app.find_by_id(
            competition_id
        )

        if competition is None:
            print("Соревнование не найдено.")
            return

        self._print_competitions(
            [competition],
            "Найденное соревнование"
        )

    def _delete_competition(self) -> None:
        
        print("\nУДАЛЕНИЕ СОРЕВНОВАНИЯ")

        competition_id = self._read_text(
            "Введите ID соревнования: "
        )

        competition = self._app.find_by_id(
            competition_id
        )

        if competition is None:
            print("Соревнование не найдено.")
            return

        self._print_competitions(
            [competition],
            "Соревнование для удаления"
        )

        confirm = self._read_bool(
            f"Удалить '{competition.name}'? (y/n): "
        )

        if not confirm:
            print("Удаление отменено.")
            return

        try:
            self._app.remove_item(competition_id)
            print("Соревнование удалено.")

        except ItemNotFoundError as error:
            print(f"Ошибка: {error}")

    def _filter_menu(self) -> None:
        while True:
            print("""
------------------------------------------------------------------------
ФИЛЬТРАЦИЯ
1. По виду спорта
2. По статусу
3. По длительности
0. Назад
------------------------------------------------------------------------
""")

            choice = self._read_int(
                "Выберите вариант: "
            )

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

            print("Ошибка: неверный пункт.")

    def _filter_by_sport(self) -> None:
    
        sport = self._read_text(
            "Введите вид спорта: "
        )

        competitions = self._app.filter_items(
            lambda c: c.sport_type.lower() == sport.lower()
        )

        self._print_competitions(
            competitions,
            f"Соревнования по виду спорта: {sport}"
        )

    def _filter_by_status(self) -> None:

        print("Статусы:")
        print("Registration")
        print("In Progress")
        print("Completed")

        status = self._read_text(
            "Введите статус: "
        )

        competitions = self._app.filter_items(
            lambda c: c.status.lower() == status.lower()
        )

        self._print_competitions(
            competitions,
            f"Соревнования со статусом: {status}"
        )

    def _filter_by_duration(self) -> None:

        min_days = self._read_positive_int(
            "Минимум дней: "
        )

        max_days = self._read_positive_int(
            "Максимум дней: "
        )

        competitions = self._app.filter_items(
            lambda c:
            min_days <= c.get_competition_duration() <= max_days
        )

        self._print_competitions(
            competitions,
            f"Соревнования от {min_days} до {max_days} дней"
        )

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

            choice = self._read_int(
                "Выберите вариант сортировки: "
            )

            if choice == 0:
                return

            reverse = self._read_bool(
                "Сортировать по убыванию? (y/n): "
            )

            self._perform_sort(choice, reverse)

            return

    def _perform_sort(
        self,
        choice: int,
        reverse: bool
    ) -> None:
        
        key_func: Callable[[Competition], Any]
        title: str

        if choice == 1:
            key_func = lambda c: c.name
            title = "По названию"

        elif choice == 2:
            key_func = lambda c: c.start_date
            title = "По дате начала"

        elif choice == 3:
            key_func = lambda c: c.max_participants
            title = "По участникам"

        elif choice == 4:
            key_func = (
                lambda c: c.get_competition_duration()
            )
            title = "По длительности"

        else:
            print("Ошибка: неверный вариант.")
            return

        competitions = self._app.sort_items(
            key=key_func,
            reverse=reverse
        )

        self._print_competitions(
            competitions,
            f"Сортировка: {title}",
            show_key=key_func
        )

    def _exit_program(self) -> None:
       
        try:
            self._app.save_data()

            print("Данные сохранены.")
            print("Завершение программы.")

        except StorageError as error:
            print(f"Ошибка сохранения: {error}")

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

        print("-" * 95)

        header = (
            f"{'ID':<10}"
            f"{'Название':<25}"
            f"{'Спорт':<15}"
            f"{'Статус':<15}"
            f"{'Участники':<15}"
        )

        if show_key:
            header += f"{'Значение':<15}"

        print(header)
        print("-" * 95)

        for competition in competitions:
            participants = (
                f"{competition.participants_count}/"
                f"{competition.max_participants}"
            )

            row = (
                f"{competition.competition_id:<10}"
                f"{competition.name[:24]:<25}"
                f"{competition.sport_type:<15}"
                f"{competition.status:<15}"
                f"{participants:<15}"
            )

            if show_key:
                row += f"{str(show_key(competition)):<15}"

            print(row)

        print("-" * 95)

    def _read_text(
        self,
        prompt: str
    ) -> str:
        
        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("Ошибка: строка не может быть пустой.")

    def _read_int(
        self,
        prompt: str
    ) -> int:
       
        while True:
            value = input(prompt).strip()

            try:
                return int(value)

            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_int_in_range(
        self,
        prompt: str,
        min_value: int,
        max_value: int
    ) -> int:
       
        while True:
            value = self._read_int(prompt)

            if min_value <= value <= max_value:
                return value

            print(
                f"Ошибка: число должно быть "
                f"от {min_value} до {max_value}."
            )

    def _read_positive_int(
        self,
        prompt: str
    ) -> int:
    
        while True:
            value = self._read_int(prompt)

            if value > 0:
                return value

            print("Ошибка: число должно быть больше 0.")

    def _read_positive_float(
        self,
        prompt: str
    ) -> float:

        while True:
            raw_value = input(prompt).strip().replace(",", ".")

            try:
                value = float(raw_value)

            except ValueError:
                print("Ошибка: введите число.")
                continue

            if value <= 0:
                print("Ошибка: число должно быть больше 0.")
                continue

            return value

    def _read_bool(
        self,
        prompt: str
    ) -> bool:
        while True:
            value = input(prompt).strip().lower()

            if value in {"y", "yes", "да", "д"}:
                return True

            if value in {"n", "no", "нет", "н"}:
                return False

            print("Ошибка: введите y/n.")

    def _read_date(
        self,
        prompt: str
    ) -> str:
        
        while True:
            value = input(prompt).strip()

            parts = value.split("-")

            if len(parts) != 3:
                print(
                    "Ошибка: используйте формат "
                    "ГГГГ-ММ-ДД."
                )
                continue

            try:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])

            except ValueError:
                print("Ошибка: неверная дата.")
                continue

            if not (1 <= month <= 12):
                print("Ошибка: неверный месяц.")
                continue

            if not (1 <= day <= 31):
                print("Ошибка: неверный день.")
                continue

            return value


