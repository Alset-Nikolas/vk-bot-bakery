from models import session, Product, Section
from models.section import get_section


def get_product_by_section(context):
    section = get_section(context['section'])
    return [item[0] for item in session.query(Product.name).filter(Product.section_id == section.id).all()]


def get_all_section(context):
    return [item[0] for item in session.query(Section.name).all()]
