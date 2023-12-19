import datetime
import json
from pathlib import Path

import aiohttp
from sqlalchemy import *
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine("postgresql+psycopg2://test:Some_password@localhost/test_base")
session = Session(bind=engine)
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()

from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = 'user_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False)
    username = Column(String(150), nullable=False, unique=True)

class Basket(Base):
    __tablename__ = 'Basket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_bot.id'), nullable=False)
    goods_id = Column(Integer, nullable=False)


class Favorites(Base):
    __tablename__ = 'Favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_bot.id'), nullable=False)
    goods_id = Column(Integer, nullable=False)


class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username_customer = Column(String(100), nullable=False)
    paied = Column(Boolean, default=False)
    text_about = Column(Text, nullable=False)
    final_price = Column(Float, nullable=False)

class Goods(Base):
    __tablename__ = 'Goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    desc = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    sale = Column(Float, default=1.0)
    size = Column(String(100), nullable=True)
    count = Column(Integer, nullable=True)
    cat = Column(Integer, nullable=False)
    pic = Column(Text, nullable=True)

class Categories(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    family = Column(Integer, default=None)

class Admins(Base):
    __tablename__ = 'Admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)


Base.metadata.create_all(engine)

def get_user(user):
    res = session.query(User).filter(User.username == user.username).first()
    adm = None
    try:
        adm = session.query(Admins).filter(Admins.name == user.username).first()
    except:
        pass
    if not res:
        new = User(username=user.username, tg_id=user.id)
        session.add(new)
        session.commit()
        return False
    elif adm:
        return True
    else:
        return False

def extract_value(input_text, keyword):
    start_index = input_text.find(keyword)
    if start_index != -1:
        end_index = input_text.find(';', start_index)
        if end_index != -1:
            return input_text[start_index + len(keyword):end_index].strip()