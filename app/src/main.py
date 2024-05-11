from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import engine
from src.routers import users
from src.dependencies import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.get('/')
def get_root():
    return RedirectResponse('/docs/')


app.include_router(users.router, prefix='/users', tags=['Пользователи'])


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
