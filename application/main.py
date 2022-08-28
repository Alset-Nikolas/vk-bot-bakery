import argparse
from log import logger
from bot.bot import Bot
import settings
from models import init_db
from models.section import add_new_section
from models.product import add_product_by_name_section
import os


def parse_args():
    """Парсер для аргумента --token и --group_id"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--group_id", type=int, required=True)
    return parser.parse_args()


def main():
    """Start the application."""
    logger.info('application run')
    if os.path.exists('secrets.py'):
        import secrets
        logger.info('Файл secrets.py найден!')
        bot = Bot(secrets.TOKEN, secrets.GROUP_ID)
    else:
        logger.warning('Файл secrets.py не найден! Проверяем ввод параметров')
        args = parse_args()
        bot = Bot(args.token, args.group_id)
    bot.run()


def fill_db():
    """
        Заполнить БД
    """
    logger.info("fill db")
    for new_section in settings.SECTIONS:
        add_new_section(**new_section)
    for new_product in settings.PRODUCTS:
        add_product_by_name_section(**new_product)


if __name__ == '__main__':
    init_db()
    fill_db()
    main()
