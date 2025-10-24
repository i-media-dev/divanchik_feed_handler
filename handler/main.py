import logging

from handler.constants import FEEDS_FOLDER
from handler.custom_labels import CUSTOM_LABELS
from handler.decorators import time_of_script
from handler.feeds_handler import FeedHandler
from handler.feeds_save import FeedSave
from handler.logging_config import setup_logging
from handler.utils import get_filenames_set

setup_logging()


@time_of_script
def main():
    try:
        save_client = FeedSave()
        save_client.save_xml()
        filenames = get_filenames_set(FEEDS_FOLDER)

        for filename in filenames:
            for custom_label in CUSTOM_LABELS:
                handler_client = FeedHandler(filename, custom_label)
                print(handler_client)
                handler_client.add_custom_label()

    except Exception as error:
        logging.error('Неожиданная ошибка: %s', error)
        raise


if __name__ == '__main__':
    main()
