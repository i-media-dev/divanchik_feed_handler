import logging

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
        handler_client.add_custom_label()
    except Exception as error:
        logging.error('Неожиданная ошибка: %s', error)
        raise


if __name__ == '__main__':
    main()
