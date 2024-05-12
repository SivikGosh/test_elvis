from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud
from src.dependencies import get_db
from src.models import Reward, RewardUser
from src.schemas import RewardAdd, RewardGet, RewardUserAdd, RewardUserGet
from src.config import SECRET
from src.logger import logger

router = APIRouter()


@router.post('/', response_model=RewardAdd)
def add_reward(
    reward: RewardAdd,
    db: Session = Depends(get_db),
    secret: str = None
):

    """Добавить достижение."""

    if secret is None:
        logger.warning('Не введён секретный ключ. (?secret=)')
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Не введён секретный ключ.'
        )

    if secret != SECRET:
        logger.warning('Введён неправильный секретный ключ.')
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Секретный ключ неверный.'
        )

    logger.info('Добавление достижения.')

    return crud.add_reward(db=db, reward=reward)


@router.get('/', response_model=list[RewardGet])
def get_rewards(db: Session = Depends(get_db)):

    """Добавить список достижений."""

    logger.info('Запрошен список достижений.')

    return db.query(Reward).all()


@router.get('/{id}', response_model=RewardGet)
def get_reward(id: int, db: Session = Depends(get_db)):

    """Получить достижение по ID."""

    reward = crud.get_reward(db=db, id=id)

    if reward is None:
        logger.info('Запрошено несуществующее достижение.')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Достижение не найдено.'
        )

    logger.info(f'Запрос достижения {reward.title}.')

    return reward


@router.post('/reward_user/', response_model=RewardUserAdd)
def reward_user(
    rewarding: RewardUserAdd,
    db: Session = Depends(get_db),
    secret: str = None
):

    """Выдать пользователю достижение."""

    if secret is None:
        logger.warning('Не введён секретный ключ. (?secret=)')
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Не введён секретный ключ.'
        )

    if secret != SECRET:
        logger.warning('Введён неправильный секретный ключ.')
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Секретный ключ неверный.'
        )

    logger.info('Награждение пользователя.')

    return crud.reward_user(db=db, rewarding=rewarding)


@router.get('/board/', response_model=list[RewardUserGet])
def get_rewarding_board(db: Session = Depends(get_db)):

    """Получить список присвоенных достижений."""

    logger.info('Запрос списка выданных достижений.')

    return db.query(RewardUser).all()
