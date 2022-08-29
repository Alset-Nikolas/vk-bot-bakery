from models.product import get_info_product_by_id
from models.user import get_state_user
from models import UserState
import typing

"""
    Обработчики сложных ответов бота пользователю
    ____________________________________________
"""


def send_product_info(user_id: int) -> typing.Dict[str, str]:
    user: UserState = get_state_user(user_id)
    description, photo_url = get_info_product_by_id(user.context['product_id'])
    return {'text': f'Описание:\n{description}', 'image': photo_url}

