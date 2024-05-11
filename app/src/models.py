from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    language = Column(Enum('ru', 'en', name='language'))


class Reward(Base):
    __tablename__ = 'rewards'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    score = Column(Integer)
    description = Column(String)


class RewardUser(Base):
    __tablename__ = 'rewardings'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    reward = Column(Integer, ForeignKey('rewards.id'))
    gave_at = Column(DateTime, default=datetime.now)
