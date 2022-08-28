from models import session, Product, Section
from models.section import get_section
import typing

"""
    Обработчики событий в сценарии, где нужна клавиатура с кнопками
    ____________________________________________________________________
"""


def get_product_by_section(context: typing.Dict[str, str]) -> typing.List[str]:
    """
        Вернуть продукты определенной секции
    """
    section = get_section(context['section'])
    return [item[0] for item in session.query(Product.name).filter(Product.section_id == section.id).all()]


def get_all_section(context: typing.Dict[str, str]) -> typing.List[str]:
    """
            Вернуть все секции
    """
    return [item[0] for item in session.query(Section.name).all()]
