from models import session, Section
from log import logger



def get_section(name):
    return session.query(Section).filter(Section.name == name).first()


def add_new_section(name):
    if get_section(name) is None:
        logger.info(f'add_new_section, name={name}')
        new_section = Section(name=name)
        session.add(new_section)
        session.commit()
