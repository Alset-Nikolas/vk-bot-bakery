from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Integer,
    String,
    Column,
    create_engine,
    ForeignKeyConstraint,
    JSON
)
from log import logger

NAME_DB = "bakery.db"
Base = declarative_base()
engine = create_engine(f"sqlite:///{NAME_DB}" + "?check_same_thread=False")
session = Session(bind=engine)


class UserState(Base):
    __tablename__ = 'user_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    scenario_name = Column(String, nullable=True)
    step_name = Column(String, nullable=True)
    context = Column(JSON, default=dict())


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    products = relationship(
        "Product", back_populates="section", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    photo_url = Column(String, nullable=False, unique=True)

    section_id = Column(Integer, nullable=False)
    section = relationship("Section", back_populates="products")

    __table_args__ = (
        ForeignKeyConstraint(["section_id"], ["sections.id"]),
    )


def init_db() -> None:
    logger.info("init data base")
    import os
    if os.path.exists(NAME_DB):
        os.remove(NAME_DB)
    Base.metadata.create_all(engine)
