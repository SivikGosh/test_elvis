from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Language(str, Enum):
    ru = 'ru'
    en = 'en'


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
    reward: int


class RewardUserAdd(RewardUserBase):
    pass


class RewardUserGet(RewardUserBase):
    id: int
    gave_at: datetime


class RewardestUser(BaseModel):
    user: UserGet
    rewards: int


class MaxScoreUser(BaseModel):
    user: UserGet
    scores: int


class MostDifference(BaseModel):
    max_user: UserGet
    max_scores: int
    min_user: UserGet
    min_scores: int
    difference: int


class LessDifference(BaseModel):
    first_user: UserGet
    first_user_scores: int
    second_user: UserGet
    second_user_scores: int
    difference: int


class UserRewardsGet(BaseModel):
    user: UserGet
    rewards: list[RewardGet]
