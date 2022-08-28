from models import Product, session, Section
from models.section import get_section
from log import logger
import typing

"""
    Модуль взаимодействия с таблицей Product
    ___________________________________________
"""


def get_product(name: str) -> typing.Optional[Product]:
    """
        Вернет продукт по имени
    """
    return session.query(Product).filter(Product.name == name).first()


def add_product_by_id_section(name: str, description: str, photo_url: str, section_id: int) -> None:
    """
        Добавить новый продукт по id секции
    """
    if get_product(name) is None:
        logger.info(f'add_product_by_id_section name={name}')
        product = Product(name=name, description=description, photo_url=photo_url, section_id=section_id)
        session.add(product)
        session.commit()


def add_product_by_name_section(name: str, description: str, photo_url: str, section_name: str) -> None:
    """
        Добавить новый продукт по названию секции
    """
    section: typing.Optional[Section] = get_section(section_name)
    if section:
        add_product_by_id_section(name, description, photo_url, section.id)
    else:
        logger.debug(f'name={name} section is not exist')


def get_info_product_by_id(product_id: int) -> typing.Tuple[typing.Optional[str], typing.Optional[str]]:
    """
        Вернуть информацию продукта по id продукта
    """
    product: typing.Optional[Product] = session.query(Product).filter(Product.id == product_id).first()
    if product:
        return product.description, product.photo_url
    return None, None
