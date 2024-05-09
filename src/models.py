from datetime import datetime
from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Integer, String, Table
)

from src.database import Base

user_chievement = Table(
    'user_achievement',
    Base.metadata,
    Column('user', Integer, ForeignKey('users.id')),
    Column('achievement', Integer, ForeignKey('achievements.id')),
    Column('rewarded_at', DateTime, default=datetime.now)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    language = Column(Enum('russian', 'english', name='language'))


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    score = Column(Integer)
    description = Column(String)
