from models import Product, session
from models.section import get_section
from log import logger


def get_product(name):
    return session.query(Product).filter(Product.name == name).first()


def add_product_by_id_section(name, description, photo_url, section_id):
    if get_product(name) is None:
        logger.info(f'add_product_by_id_section name={name}')
        product = Product(name=name, description=description, photo_url=photo_url, section_id=section_id)
        session.add(product)
        session.commit()


def add_product_by_name_section(name, description, photo_url, section_name):
    section = get_section(section_name)
    if section:
        add_product_by_id_section(name, description, photo_url, section.id)
    else:
        logger.debug(f'name={name} section is not exist')


def get_info_product_by_id(product_id):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        return product.description, product.photo_url
