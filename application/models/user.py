from models import session, UserState
import settings
from sqlalchemy.orm.attributes import flag_modified


def get_state_user(user_id):
    return session.query(UserState).filter(UserState.user_id == user_id).first()


def next_step(user_id):
    state = get_state_user(user_id)
    next_step = settings.SCENARIOS[state.scenario_name]['steps'][state.step_name]['next_step']
    if next_step is None:
        session.delete(state)
    else:
        state.step_name = next_step
    session.commit()
    return next_step is not None


def back_step(user_id):
    state = get_state_user(user_id)
    new_step = settings.SCENARIOS[state.scenario_name]['steps'][state.step_name]['jump_back_step']
    if new_step is None:
        return
    state.step_name = new_step
    session.add(state)
    session.commit()


def registration(user_id, scenario, first_step):
    new_user = UserState(user_id=user_id, scenario_name=scenario, step_name=first_step)
    session.add(new_user)
    session.commit()


def update_context(user_id, key, value):
    user = get_state_user(user_id)
    if key not in user.context:
        user.context[key] = ''
    user.context[key] = value
    flag_modified(user, "context")
    session.add(user)
    session.commit()
