from models.section import get_section
from models.product import get_product
from models.user import update_context, back_step

"""
    Обработчики валидности ответов пользователя
    ____________________________________________
"""


def handlers_section(section_name: str, user_id: int) -> bool:
    """
        Обработчик имени секции (есть ли такая)
    """
    if get_section(section_name) is not None:
        update_context(user_id=user_id, key='section', value=section_name)
        return True
    if section_name == 'Назад':
        back_step(user_id)
    return False


def handlers_product(product_name: str, user_id: int) -> bool:
    """
        Обработчик имени продукта (есть ли такой)
    """
    product = get_product(product_name)
    if product is not None:
        update_context(user_id=user_id, key='product_id', value=product.id)
        return True
    if product_name == 'Назад':
        back_step(user_id)
        return True
    return False
