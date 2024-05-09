from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Language(str, Enum):
    russian = 'russian'
    english = 'english'


class UserBase(BaseModel):
    name: str
    language: Language


class UserAdd(UserBase):
    pass


class UserGet(UserBase):
    id: int
    name: str
    language: Language

    class Config:
        from_attributes = True


class RewardBase(BaseModel):
    title: str
    score: int
    description: str


class RewardAdd(RewardBase):
    pass


class RewardGet(RewardBase):
    id: int

    class Config:
        from_attributes = True


class RewardUserBase(BaseModel):
    user: int


class RewardUserAdd(RewardUserBase):
    reward: int


class RewardUserGet(RewardUserBase):
    id: int
    reward: int
    gave_at: datetime


class RewardestUser(RewardUserBase):
    rewards: Optional[int]
