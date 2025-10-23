import logging

from handler.custom_labels import CUSTOM_LABELS
from handler.decorators import time_of_script
from handler.feeds_handler import FeedHandler
from handler.feeds_save import FeedSave
from handler.logging_config import setup_logging

setup_logging()


@time_of_script
def main():
    try:
        save_client = FeedSave()
        handler_client = FeedHandler()

        save_client.save_xml()
        for label in CUSTOM_LABELS:
            label = handler_client._get_custom_labels(label)
            name_label = handler_client._add_name_cl_file(label)
            parse_cl = handler_client._parse_custom_labels(label)
            handler_client._save_custom_label(name_label, parse_cl)
    except Exception as error:
        logging.error('Неожиданная ошибка: %s', error)
        raise


if __name__ == '__main__':
    main()
