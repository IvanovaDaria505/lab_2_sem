class AppError(Exception):
    pass

class ItemNotFoundError(AppError):
    pass

class DuplicateItemError(AppError):
    pass

class StorageError(AppError):
    pass