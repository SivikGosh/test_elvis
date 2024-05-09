from sqlalchemy.orm import Session

from src import models, schemas


def add_user(db: Session, user: schemas.UserAdd):
    user = models.User(name=user.name, language=user.language)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def add_achievement(db: Session, achievement: schemas.AchievementAdd):
    achievement = models.Achievement(
        title=achievement.title,
        score=achievement.score,
        description=achievement.description
    )
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return achievement


def get_achievement(db: Session, id: int):
    return (
        db.query(models.Achievement)
        .filter(models.Achievement.id == id)
        .first()
    )
