import os

from dotenv import load_dotenv

load_dotenv()

TAG_NAME = {
    'new': 'custom_label_1',
    'top': 'custom_label_2'
}
"""Название тега в зависимости от названия файла."""

DATE_FORMAT = '%Y-%m-%d'
"""Формат даты по умолчанию."""

TIME_FORMAT = '%H:%M:%S'
"""Формат времени по умолчанию."""

PROTOCOL = 'https'
"""Протокол запроса."""

ADDRESS = 'projects/globus/new_images'
"""Путь к файлу."""

DOMEN_FTP = 'feeds.i-media.ru'
"""Домен FTP-сервера."""

NAME_OF_SHOP = 'divanchik'
"""Константа названия магазина."""

FEEDS_FOLDER = os.getenv('FEEDS_FOLDER', 'temp_feeds')
"""Константа стокового названия директории с фидами."""

NEW_FEEDS_FOLDER = os.getenv('NEW_FEEDS_FOLDER', 'new_feeds')
"""Константа стокового названия директории с измененными фидами."""

ENCODING = 'utf-8'
"""Кодировка по умолчанию."""
