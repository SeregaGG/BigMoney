from typing import get_type_hints
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Text, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL

url_object = URL.create(
    "postgresql",
    username="username",
    password="password",
    host="147.45.245.163",
    database="bigmoney",
)

Base = declarative_base()

class Users(Base):
    __tablename__ = 'testtable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

main_engine = create_engine(url_object)

DBSession = sessionmaker(
    binds={
        Base: main_engine,
    },
    expire_on_commit=False,
)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
app = FastAPI()



class User(BaseModel):
    user_id: int

@app.get("/users/")
def root():
    with session_scope() as s:
        result = s.query(Users).all()
    return result