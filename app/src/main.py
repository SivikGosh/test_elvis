from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src import models
from src.database import engine
from src.routers import users, rewards
import logging

logger = logging.basicConfig(
    'logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def get_root():
    return RedirectResponse(url=app.docs_url)


app.include_router(users.router, prefix='/users', tags=['Пользователи'])
app.include_router(rewards.router, prefix='/rewards', tags=['Достижения'])
