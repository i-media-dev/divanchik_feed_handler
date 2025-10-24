import logging
from pathlib import Path

from handler.exceptions import (DirectoryCreationError, EmptyFeedsListError)
from handler.logging_config import setup_logging

setup_logging()


def get_filenames_set(folder_name: str) -> set[str]:
    """Функция возвращает множество названий фидов."""
    folder_path = Path(__file__).parent.parent / folder_name
    if not folder_path.exists():
        logging.error('Папка %s не существует', folder_name)
        raise DirectoryCreationError('Папка %s не найдена', folder_name)
    files_names = {
        file.name for file in folder_path.iterdir() if file.is_file()
    }
    if not files_names:
        logging.error('В папке нет файлов')
        raise EmptyFeedsListError('Нет скачанных файлов')
    logging.debug('Найдены файлы: %s', files_names)
    return files_names
