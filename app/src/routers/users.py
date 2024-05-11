from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud
from src.dependencies import get_db
from src.models import User
from src.schemas import (
    LessDifference,
    MaxScoreUser,
    MostDifference,
    RewardestUser,
    RewardGet,
    UserAdd,
    UserGet,
)

router = APIRouter()


@router.post('/', response_model=UserAdd)
def add_user(user: UserAdd, db: Session = Depends(get_db)):
    return crud.add_user(db=db, user=user)


@router.get('/', response_model=list[UserGet])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get('/{id}', response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Пользователь не найден.'
        )
    return user


@router.get('/rewardest/', response_model=RewardestUser)
def get_rewardest_user(db: Session = Depends(get_db)):
    user, rewards = crud.get_rewardest_user(db=db)
    return {'user': user, 'rewards': rewards}


@router.get('/max_scores/', response_model=MaxScoreUser)
def get_user_with_max_scores(db: Session = Depends(get_db)):
    user, scores = crud.get_user_with_max_scores(db=db)
    return {'user': user, 'scores': scores}


@router.get('/most_difference/', response_model=MostDifference)
def get_users_with_most_difference(db: Session = Depends(get_db)):
    user_max, score_max, user_min, score_min, difference = (
        crud.get_users_with_most_difference(db=db)
    )
    return {
        'user_max': user_max,
        'user_max_score': score_max,
        'user_min': user_min,
        'user_min_score': score_min,
        'difference': difference
    }


@router.get('/less_difference/', response_model=LessDifference)
def get_users_with_less_difference(db: Session = Depends(get_db)):
    (
        first_user,
        first_user_scores,
        second_user,
        second_user_scores,
        difference
    ) = crud.get_users_with_less_difference(db=db)
    return {
        'first_user': first_user,
        'first_user_scores': first_user_scores,
        'second_user': second_user,
        'second_user_scores': second_user_scores,
        'difference': difference
    }


@router.get('/rewarded_for_week/', response_model=list[UserGet])
def get_users_rewarded_for_week(db: Session = Depends(get_db)):
    rewards = crud.get_users_rewarded_for_week(db=db)
    return rewards


@router.get('/{id}/rewards/', response_model=list[RewardGet])
def get_user_rewards(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Пользователь не найден.'
        )
    else:
        user = crud.get_user_rewards(db=db, id=id)
    return user
