from sqlalchemy.orm import Session

from src import models, schemas
# from sqlalchemy import func


def add_user(db: Session, user: schemas.UserAdd):
    user = models.User(name=user.name, language=user.language)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def add_reward(db: Session, reward: schemas.RewardAdd):
    reward = models.Reward(
        title=reward.title, score=reward.score, description=reward.description
    )
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def get_reward(db: Session, id: int):
    return db.query(models.Reward).filter(models.Reward.id == id).first()


def reward_user(db: Session, rewarding: schemas.RewardUserAdd):
    rewarding = models.RewardUser(user=rewarding.user, reward=rewarding.reward)
    db.add(rewarding)
    db.commit()
    db.refresh(rewarding)
    return rewarding


def get_rewardest_user(db: Session):
    pass
