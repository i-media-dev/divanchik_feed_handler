class EmptyXMLError(ValueError):
    """Ошибка пустого XML-файла."""


class InvalidXMLError(ValueError):
    """Ошибка невалидного XML-файла."""


class TableNameError(ValueError):
    """Ошибка отсутствующей таблицы."""


class EmptyFeedsListError(ValueError):
    """Ошибка пустой коллекции с фидами."""


class DirectoryCreationError(ValueError):
    """Ошибка создания дериктории."""


class GetTreeError(ValueError):
    """Ошибка получения дерева XML-файла."""


class StructureXMLError(ValueError):
    """Ошибка структуры XML-файла."""


class MissingFolderError(Exception):
    """Ошибка отсутствующей директории."""


class ValidationLabelError(Exception):
    """Ошибка валидации custom_label."""


class EmptyLabelTupleError(ValueError):
    """Ошибка пустой коллекции с custom_label."""
