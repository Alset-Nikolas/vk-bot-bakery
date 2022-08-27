import argparse
from log import logger
from bot.bot import Bot
import settings
from models import init_db
from models.section import add_new_section
from models.product import add_product_by_name_section
import secrets

def parse_args():
    """Парсер для аргумента --token"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--group_id", type=int, required=True)
    return parser.parse_args()


def main():
    """Start the application."""
    logger.info('application run')
    # args = parse_args()
    bot = Bot(secrets.TOKEN, secrets.GROUP_ID)
    bot.run()


def fill_db():
    for new_section in settings.SECTIONS:
        add_new_section(**new_section)
    for new_product in settings.PRODUCTS:
        add_product_by_name_section(**new_product)



if __name__ == '__main__':
    init_db()
    fill_db()
    main()
