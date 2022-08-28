from models import session, UserState
import settings
from sqlalchemy.orm.attributes import flag_modified
import typing

"""
    Модуль взаимодействия с таблицей UserState 
    ___________________________________________
"""


def get_state_user(user_id: int) -> UserState:
    """
        Функция вернет состояние пользователя по id
    """
    return session.query(UserState).filter(UserState.user_id == user_id).first()

def delete_user_state(user_id: int )->None:
    """
        Функция удаления пользователя
    """
    state: UserState = get_state_user(user_id)
    session.delete(state)
    session.commit()

def next_step(user_id: int) -> bool:
    """
        Функция перехода на следующий шаг по сценарию
    """
    state: UserState = get_state_user(user_id)
    name_next_step: typing.Optional[str] = settings.SCENARIOS[state.scenario_name]['steps'][state.step_name][
        'next_step']
    if name_next_step is None:
        delete_user_state(user_id)
    else:
        state.step_name = name_next_step
        session.commit()
    return next_step is not None


def back_step(user_id: int) -> None:
    """
        Функция перехода на предыдущий шаг по сценарию
    """
    state: UserState = get_state_user(user_id)
    new_step: str = settings.SCENARIOS[state.scenario_name]['steps'][state.step_name]['jump_back_step']
    if new_step is None:
        return
    state.step_name = new_step
    session.add(state)
    session.commit()


def registration(user_id: int, scenario: str, first_step: str) -> None:
    """
        Регистрация пользователя
    """
    new_user: UserState = UserState(user_id=user_id, scenario_name=scenario, step_name=first_step)
    session.add(new_user)
    session.commit()


def update_context(user_id: int, key: str, value: str) -> None:
    """
        Обновления контекста у пользователя
    """
    user: UserState = get_state_user(user_id)
    if key not in user.context:
        user.context[key] = ''
    user.context[key] = value
    flag_modified(user, "context")
    session.add(user)
    session.commit()
