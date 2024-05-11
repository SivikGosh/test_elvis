from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud
from src.dependencies import get_db
from src.models import Reward, RewardUser
from src.schemas import RewardAdd, RewardGet, RewardUserAdd, RewardUserGet

router = APIRouter()


@router.post('/', response_model=RewardAdd)
def add_reward(reward: RewardAdd, db: Session = Depends(get_db)):
    return crud.add_reward(db=db, reward=reward)


@router.get('/', response_model=list[RewardGet])
def get_rewards(db: Session = Depends(get_db)):
    return db.query(Reward).all()


@router.get('/{id}', response_model=RewardGet)
def get_reward(id: int, db: Session = Depends(get_db)):
    reward = crud.get_reward(db=db, id=id)
    if reward is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Достижение не найдено.'
        )
    return reward


@router.post('/reward_user/', response_model=RewardUserAdd)
def reward_user(
    rewarding: RewardUserAdd, db: Session = Depends(get_db)
):
    return crud.reward_user(db=db, rewarding=rewarding)


@router.get('/board/', response_model=list[RewardUserGet])
def get_rewarding_board(db: Session = Depends(get_db)):
    return db.query(RewardUser).all()