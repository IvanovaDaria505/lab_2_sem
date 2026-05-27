"""
Пользовательские исключения для предметной области.
"""

class AppError(Exception):
    """Базовое исключение приложения."""
    pass

class ItemNotFoundError(AppError):
    """Объект не найден в коллекции."""
    pass

class DuplicateItemError(AppError):
    """Объект с таким идентификатором уже существует."""
    pass

class StorageError(AppError):
    """Ошибка при работе с хранилищем данных."""
    pass