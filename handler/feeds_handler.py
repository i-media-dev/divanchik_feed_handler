import logging
import re
import xml.etree.ElementTree as ET

import requests

from custom_labels.new import NEW
from custom_labels.top import TOP
from handler.constants import (FEEDS_FOLDER, LABELS_FOLDER, NEW_FEEDS_FOLDER,
                               TAG_NAME)
from handler.decorators import time_of_function
from handler.exceptions import EmptyLabelTupleError, ValidationLabelError
from handler.logging_config import setup_logging
from handler.mixins import FileMixin

setup_logging()
logger = logging.getLogger(__name__)


class FeedHandler(FileMixin):
    """
    Класс, предоставляющий интерфейс
    для обработки xml-файлов.
    """

    def __init__(
        self,
        filename: str,
        custom_labels_urls: tuple,
        labels_folder: str = LABELS_FOLDER,
        feeds_folder: str = FEEDS_FOLDER,
        new_feeds_folder: str = NEW_FEEDS_FOLDER
    ) -> None:
        self.filename = filename
        self.custom_labels_urls = custom_labels_urls
        self.labels_folder = labels_folder
        self.feeds_folder = feeds_folder
        self.new_feeds_folder = new_feeds_folder

    def __repr__(self):
        return (
            f"FeedHandler(filename = '{self.filename}', "
            f"custom_labels_urls='{self.custom_labels_urls}', "
            f"labels_folder='{self.labels_folder}', "
            f"feeds_folder='{self.feeds_folder}', "
            f"new_feeds_folder='{self.new_feeds_folder}')"
        )

    def _save_xml(
        self,
        elem,
        file_folder: str,
        filename: str,
    ) -> None:
        """Защищенный метод, сохраняет отформатированные файлы."""
        root = elem
        self._indent(root)
        formatted_xml = ET.tostring(root, encoding='windows-1251')
        file_path = self._make_dir(file_folder)
        with open(
            file_path / f'{filename}',
            'wb'
        ) as f:
            f.write(formatted_xml)

    def _add_name_label_file(self, label_text) -> str:
        """Защищенный метод, дает имя файла custom_label."""
        try:
            return 'new.py' if 'new' in label_text else 'top.py'
        except Exception as error:
            logging.error('Неожиданная ошибка определения имени: %s', error)
            return ''

    def _get_custom_labels(self, labels_urls: tuple) -> list | None:
        """Защищенный метод, получает custom_label по ссылке."""
        try:
            result = []
            for label_url in labels_urls:
                response = requests.get(
                    label_url,
                    stream=True,
                    timeout=(10, 60)
                )
                if response.status_code == requests.codes.ok:
                    result.append(response.text)
                else:
                    logging.error(
                        'HTTP ошибка %s при загрузке %s',
                        response.status_code,
                        label_url
                    )
                    return []
            return result
        except requests.RequestException as error:
            logging.error('Ошибка при загрузке %s: %s', label_url, error)
            return []
        except Exception as error:
            logging.error('Неожиданная ошибка: %s', error)
            return []

    def _save_custom_label(self, filename: str, custom_label: tuple) -> None:
        """Защищенный метод, сохраняет файл custom_label."""
        try:
            folder_path = self._make_dir(self.labels_folder)
            with open(folder_path / filename, 'w', encoding='utf-8') as f:
                f.write(f'{filename.split('.')[0].upper()} = {custom_label}\n')
        except Exception as error:
            logging.error('Неожиданная ошибка при сохранении: %s', error)

    def _validate(self, custom_label: tuple):
        """Защищенный метод валидации кортежа."""
        if not custom_label:
            raise EmptyLabelTupleError('Кортеж айдишников пуст')

        total_length = sum(len(str(item)) for item in custom_label)
        avg_length = total_length // len(custom_label)

        suspicious_items = []
        for item in custom_label:
            item_length = len(str(item))
            if item_length > avg_length * 2:
                suspicious_items.append((item, item_length, avg_length))

        if suspicious_items:
            logging.warning(
                'Обнаружены подозрительно длинные элементы: %s',
                suspicious_items
            )
            raise ValidationLabelError(
                f'Большая вероятность пропущенной запятой: {suspicious_items}'
            )

    def _parse_custom_labels(self, label_text: str) -> tuple:
        """Защищенный метод, парсит текст и извлекает данные."""
        try:
            matches = re.findall(r"'(\d+)'", label_text)
            return tuple(matches)
        except Exception as error:
            logging.error('Ошибка парсинга данных: %s', error)
            return ()

    def _paste_custom_label(
        self,
        offers: list,
        custom_label: tuple,
        text_tag: str,
        name_tag: str
    ) -> None:
        """Защищенный метод, вставляет валидные теги в файл."""
        for offer in offers:
            offer_id = str(offer.get('id'))
            custom_label_tag = ET.SubElement(
                offer,
                name_tag
            )
            if offer_id in custom_label:
                custom_label_tag.text = text_tag.capitalize()
            else:
                custom_label_tag.text = 'all'

    @time_of_function
    def add_custom_label(self) -> None:
        """
        Метод добавления нового custom_label в оффер,
        если он валиден, в противном случае - берет крайний валидный вариант.
        """
        label_list = self._get_custom_labels(self.custom_labels_urls)
        tree = self._get_tree(self.filename, self.feeds_folder)
        root = tree.getroot()
        offers = list(root.findall('.//offer'))
        logger.bot_event(
            'Количество офферов в исходном фиде %s - %s',
            self.filename,
            len(offers)
        )
        if not label_list:
            logging.error('Не удалось получить список кастом лейблов')
            return
        for label_text in label_list:
            name_label = self._add_name_label_file(label_text)
            try:
                parse_label = ()
                try:
                    if name_label and label_text:
                        parse_label = self._parse_custom_labels(label_text)
                        self._validate(parse_label)
                        self._save_custom_label(name_label, parse_label)
                except EmptyLabelTupleError as error:
                    logging.warning(
                        'Получен пустой кортеж custom_label: %s',
                        error
                    )
                except ValidationLabelError as error:
                    logging.warning('Ошибка в полученных данных: %s', error)
                except Exception as error:
                    logging.error('Неожиданная ошибка валидации: %s', error)

                text_tag = name_label.split('.')[0]
                name_tag = TAG_NAME[text_tag]
                if not parse_label:
                    parse_label = NEW if text_tag == 'new' else TOP
                    logger.bot_event(
                        'Входящий custom_label не прошел валидацию. '
                        'Используем резервные данные для %s. '
                        'Проверьте логи для более детальной информации.',
                        text_tag
                    )
                self._paste_custom_label(
                    offers,
                    parse_label,
                    text_tag,
                    name_tag
                )

            except Exception as error:
                logging.error(
                    'Неожиданная ошибка добавления custom_label: %s',
                    error
                )
                raise

        self._save_xml(
            root,
            self.new_feeds_folder,
            self.filename
        )
        logging.info(
            'Файл %s сохранен в %s',
            self.filename,
            self.new_feeds_folder
        )
        new_tree = self._get_tree(self.filename, self.new_feeds_folder)
        new_root = new_tree.getroot()
        new_offers = list(new_root.findall('.//offer'))
        logger.bot_event(
            'Количество офферов в измененном фиде - %s',
            len(new_offers)
        )
