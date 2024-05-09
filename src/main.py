from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.UserAdd)
async def add_user(user: schemas.UserAdd, db: Session = Depends(get_db)):
    return crud.add_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.UserGet])
async def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/users/{id}', response_model=schemas.UserGet)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден.'
        )
    return user


# @app.get('/users/most_rewarded')
# async def get_most_rewarded_user():
#     """Пользователь с максимальным количеством наград."""

#     return {}


# @app.get('/users/max_scores')
# async def get_user_with_max_scores():
#     """Пользователь с максимальным количеством баллов."""

#     return {}


# @app.get('/users/most_difference')
# async def get_users_with_most_difference():
#     """Пользователи с наибольшей разницей очков."""

#     return []


# @app.get('/users/less_difference')
# async def get_users_with_less_difference():
#     """Пользователи с наименьшей разницей очков."""

#     return []


# @app.get('/users/{id}/achievements')
# async def get_user_achievements():
#     """Список достижений пользователя."""

#     return []


@app.post('/achievements/', response_model=schemas.AchievementAdd)
async def add_achievement(
    achievements: schemas.AchievementAdd, db: Session = Depends(get_db)
):
    return crud.add_achievement(db=db, achievement=achievements)


@app.get('/achievements/', response_model=list[schemas.AchievementGet])
async def get_achievements(db: Session = Depends(get_db)):
    return db.query(models.Achievement).all()


@app.get('/achievements/{id}', response_model=schemas.AchievementGet)
async def get_achievement(id: int, db: Session = Depends(get_db)):
    achievement = crud.get_achievement(db=db, id=id)
    if achievement is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Достижение не найдено.'
        )
    return achievement


# @app.post('/achievements/reward')
# async def add_user_achievement():
#     """Выдать пользователю достижение."""

#     return {'status': 200}
