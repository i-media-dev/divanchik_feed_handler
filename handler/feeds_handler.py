import json
import logging
import re
import xml.etree.ElementTree as ET

import requests

from handler.constants import FEEDS_FOLDER, NEW_FEEDS_FOLDER
from handler.custom_labels import CUSTOM_LABELS
from handler.decorators import time_of_function
from handler.logging_config import setup_logging
from handler.mixins import FileMixin

setup_logging()


class FeedHandler(FileMixin):
    """
    Класс, предоставляющий интерфейс
    для обработки xml-файлов.
    """

    def __init__(
        self,
        feeds_folder: str = FEEDS_FOLDER,
        new_feeds_folder: str = NEW_FEEDS_FOLDER
    ) -> None:
        self.feeds_folder = feeds_folder
        self.new_feeds_folder = new_feeds_folder

    def _save_xml(
        self,
        elem,
        file_folder: str,
        filename: str,
        prefix='new_'
    ) -> None:
        """Защищенный метод, сохраняет отформатированные файлы."""
        root = elem
        self._indent(root)
        formatted_xml = ET.tostring(root, encoding='unicode')
        file_path = self._make_dir(file_folder)
        with open(
            file_path / f'{prefix}{filename}',
            'w',
            encoding='utf-8'
        ) as f:
            f.write(formatted_xml)

    def _validate(self):
        pass

    def _add_name_cl_file(self, text):
        """Защищенный метод, дает имя файла custom_label."""
        try:
            return 'new.json' if 'new' in text else 'top.json'
        except Exception as error:
            logging.error('Неожиданная ошибка определения имени: %s', error)
            return ''

    def _get_custom_labels(self, label):
        """Защищенный метод, получает custom_label по ссылке."""
        try:
            response = requests.get(label, stream=True, timeout=(10, 60))

            if response.status_code == requests.codes.ok:
                return response.text
            else:
                logging.error(
                    'HTTP ошибка %s при загрузке %s',
                    response.status_code,
                    label
                )
                return None
        except requests.RequestException as error:
            logging.error('Ошибка при загрузке %s: %s', label, error)
            return None
        except Exception as error:
            logging.error('Неожиданная ошибка: %s', error)
            return None

    def _save_custom_label(self, filename, custom_label):
        """Защищенный метод, сохраняет файл custom_label."""
        try:
            folder_path = self._make_dir('custom_labels')
            json_key = filename.split('.')[0]
            with open(folder_path / filename, 'w', encoding='utf-8') as f:
                json.dump({json_key: custom_label}, f, indent=2)
        except Exception as error:
            logging.error('Неожиданная ошибка при сохранении: %s', error)

    def _parse_custom_labels(self, text):
        """Защищенный метод, парсит текст и извлекает данные."""
        try:
            matches = re.findall(r"'(\d+)'", text)
            print(tuple(matches))
            return tuple(matches)
        except Exception as error:
            logging.error('Ошибка парсинга данных: %s', error)
            return ()

    @time_of_function
    def add_custom_label(self):

        try:
            filenames = self._get_filenames_set(self.feeds_folder)

            for filename in filenames:
                tree = self._get_tree(filename, self.feeds_folder)
                root = tree.getroot()
                offers = list(root.findall('.//offer'))

                for offer in offers:
                    offer_id = str(offer.get('id'))

                self._save_xml(root, self.new_feeds_folder, filename)

        except Exception as error:
            logging.error('Неожиданная ошибка: %s', error)
