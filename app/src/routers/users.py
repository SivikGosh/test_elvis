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
from src.config import SECRET

router = APIRouter()


@router.post('/', response_model=UserAdd)
def add_user(user: UserAdd, db: Session = Depends(get_db), secret: str = None):

    """Добавить пользователя."""

    if secret != SECRET:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Секретный ключ неверный.'
        )

    return crud.add_user(db=db, user=user)


@router.get('/', response_model=list[UserGet])
def get_users(db: Session = Depends(get_db)):

    """Получить список пользователей."""

    return db.query(User).all()


@router.get('/{id}', response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):

    """Получить пользователя по ID."""

    user = crud.get_user(db=db, id=id)

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден.'
        )

    return user


@router.get('/rewardest/', response_model=RewardestUser)
def get_rewardest_user(db: Session = Depends(get_db)):

    """Получить пользователя с наибольшим количеством достижений."""

    return crud.get_rewardest_user(db=db)


@router.get('/max_scores/', response_model=MaxScoreUser)
def get_user_with_max_scores(db: Session = Depends(get_db)):

    """Получить пользователя с наибольшим суммой очков достижений."""

    return crud.get_user_with_max_scores(db=db)


@router.get('/most_difference/', response_model=MostDifference)
def get_users_with_most_difference(db: Session = Depends(get_db)):

    """Получить пользователей с наибольшей разницей очков достижений."""

    return crud.get_users_with_most_difference(db=db)


@router.get('/less_difference/', response_model=LessDifference)
def get_users_with_less_difference(db: Session = Depends(get_db)):

    """Получить пользователя с наименьшей разницей очков достижений."""

    return crud.get_users_with_less_difference(db=db)


@router.get('/rewarded_for_week/', response_model=list[UserGet])
def get_users_rewarded_for_week(db: Session = Depends(get_db)):

    """Получить пользователей с семидневной непрерывной серией достижений."""

    return crud.get_users_rewarded_for_week(db=db)


@router.get('/{id}/rewards/', response_model=list[RewardGet])
def get_user_rewards(id: int, db: Session = Depends(get_db)):

    """Получить достижения пользователя."""

    user = crud.get_user(db=db, id=id)

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден.'
        )
    else:
        user = crud.get_user_rewards(db=db, id=id)

    return user
