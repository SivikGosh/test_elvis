from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_NAME, DB_HOST, DB_PASS, DB_USER, DB_PORT

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
# )  # sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()