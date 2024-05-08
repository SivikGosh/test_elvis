from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

app = FastAPI()


class Language(str, Enum):
    rus = 'russian'
    eng = 'english'


class User(BaseModel):
    id: int
    name: str
    language: Language


class Achievement(BaseModel):
    id: int
    title: str
    score: int
    description: str


@app.get('/users')
async def get_users() -> RedirectResponse:
    """Список пользователей."""

    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.get('/users/{id}')
async def get_user_info(id: int):
    """Информация о пользователе."""

    return {'id': id}


@app.get('/achievements')
async def get_achievements():
    """Список достижений."""

    return []


@app.get('/achievements/{id}')
async def get_achievement_info(id: int):
    """Информация о достижении."""

    return {'id': id}


@app.post('/achievements/')
async def create_achievement():
    """Добавление достижения."""

    return {'status': 200}


@app.post('/achievements/reward')
async def add_user_achievement():
    """Выдать пользователю достижение."""

    return {'status': 200}


@app.get('/users/{id}/achievements')
async def get_user_achievements():
    """Список достижений пользователя."""

    return []


@app.get('/users/most_rewarded')
async def get_most_rewarded_user():
    """Пользователь с максимальным количеством наград."""

    return {}


@app.get('/users/max_scores')
async def get_user_with_max_scores():
    """Пользователь с максимальным количеством баллов."""

    return {}


@app.get('/users/most_difference')
async def get_users_with_most_difference():
    """Пользователи с наибольшей разницей очков."""

    return []


@app.get('/users/less_difference')
async def get_users_with_less_difference():
    """Пользователи с наименьшей разницей очков."""

    return []
