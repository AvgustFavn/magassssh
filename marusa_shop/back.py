from pathlib import Path

from sqlalchemy import *
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine("postgresql+psycopg2://test:Some_password@localhost/test_base")
session = Session(bind=engine)
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False)
    username = Column(String(150), nullable=False, unique=True)

class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username_customer = Column(String(100), nullable=False)
    status = Column(String(100), default='Создан') # Создан, Выкуплен
    text_about = Column(Text, nullable=False)
    check = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

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