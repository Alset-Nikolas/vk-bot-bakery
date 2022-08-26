import argparse
from log import logger
from bot import Bot
import settings


def parse_args():
    """Парсер для аргумента --token"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True)
    parser.add_argument("--group_id", type=int, required=True)
    return parser.parse_args()


def main():
    """Start the bot."""
    logger.info('bot run')
    # args = parse_args()
    bot = Bot(settings.TOKEN, settings.GROUP_ID)
    bot.run()


if __name__ == '__main__':
    main()
