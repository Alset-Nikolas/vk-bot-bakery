from models.section import get_section
from models.product import get_product
from models.user import update_context, back_step


def handlers_section(section_name, user_id):
    print('product', get_section(section_name), section_name)
    if get_section(section_name) is not None:
        update_context(user_id=user_id, key='section', value=section_name)
        return True
    if section_name == 'Назад':
        back_step(user_id)
    return False


def handlers_product(product_name, user_id):
    product = get_product(product_name)
    print('product', product_name)
    if product is not None:
        update_context(user_id=user_id, key='product_id', value=product.id)
        return True
    if product_name == 'Назад':
        back_step(user_id)
        return True
    return False
