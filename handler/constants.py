import os

from dotenv import load_dotenv

load_dotenv()

ATTEMPTION_LOAD_FEED = 3
"""Попытки для скачивания фида."""

DELAY_FOR_RETRY = (5, 15, 30)
"""Задержки перед переподключением."""

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

LABELS_FOLDER = os.getenv('LABELS_FOLDER', 'custom_labels')
"""Константа стокового названия директории с custon_label."""

FEEDS_FOLDER = os.getenv('FEEDS_FOLDER', 'temp_feeds')
"""Константа стокового названия директории с фидами."""

NEW_FEEDS_FOLDER = os.getenv('NEW_FEEDS_FOLDER', 'new_feeds')
"""Константа стокового названия директории с измененными фидами."""

ENCODING = 'windows-1251'
"""Кодировка по умолчанию."""
