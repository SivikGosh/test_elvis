from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

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
def add_user(user: schemas.UserAdd, db: Session = Depends(get_db)):
    return crud.add_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.UserGet])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/users/{id}', response_model=schemas.UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Пользователь не найден.'
        )
    return user


@app.get('/users/rewardest/', response_model=schemas.RewardestUser)
def get_rewardest_user(db: Session = Depends(get_db)):
    user, rewards = crud.get_rewardest_user(db=db)
    return {'user': user, 'rewards': rewards}


@app.get('/users/max_scores/', response_model=schemas.MaxScoreUser)
def get_user_with_max_scores(db: Session = Depends(get_db)):
    user, scores = crud.get_user_with_max_scores(db=db)
    return {'user': user, 'scores': scores}


# @app.get('/users/most_difference')
# def get_users_with_most_difference():
#     """Пользователи с наибольшей разницей очков."""

#     return []


# @app.get('/users/less_difference')
# def get_users_with_less_difference():
#     """Пользователи с наименьшей разницей очков."""

#     return []


# @app.get('/users/{id}/achievements')
# def get_user_rewards():

#     return []


@app.post('/rewards/', response_model=schemas.RewardAdd)
def add_reward(reward: schemas.RewardAdd, db: Session = Depends(get_db)):
    return crud.add_reward(db=db, reward=reward)


@app.get('/rewards/', response_model=list[schemas.RewardGet])
def get_rewards(db: Session = Depends(get_db)):
    return db.query(models.Reward).all()


@app.get('/rewards/{id}', response_model=schemas.RewardGet)
def get_reward(id: int, db: Session = Depends(get_db)):
    reward = crud.get_reward(db=db, id=id)
    if reward is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Достижение не найдено.'
        )
    return reward


@app.post('/reward_user/', response_model=schemas.RewardUserAdd)
def reward_user(
    rewarding: schemas.RewardUserAdd, db: Session = Depends(get_db)
):
    return crud.reward_user(db=db, rewarding=rewarding)


@app.get('/rewarding_board/', response_model=list[schemas.RewardUserGet])
def get_rewarding_board(db: Session = Depends(get_db)):
    return db.query(models.RewardUser).all()
