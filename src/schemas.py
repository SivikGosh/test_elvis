from enum import Enum
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


class AchievementBase(BaseModel):
    title: str
    score: int
    description: str


class AchievementAdd(AchievementBase):
    pass


class AchievementGet(AchievementBase):
    id: int

    class Config:
        from_attributes = True
