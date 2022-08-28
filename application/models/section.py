from models import session, Section
from log import logger
import typing
"""
    Модуль взаимодействия с таблицей Section
    ___________________________________________
"""


def get_section(name: str) -> typing.Optional[Section]:
    """
        Вернет секцию по имени
    """
    return session.query(Section).filter(Section.name == name).first()


def add_new_section(name: str) -> None:
    """
        Добавить новую секцию по имени
    """
    if get_section(name) is None:
        logger.info(f'add_new_section, name={name}')
        new_section = Section(name=name)
        session.add(new_section)
        session.commit()
