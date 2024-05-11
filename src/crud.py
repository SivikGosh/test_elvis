from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session
import mtranslate

from src import models, schemas


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
    rewardest = (
        db.query(models.RewardUser.user, func.count(models.RewardUser.reward))
        .group_by(models.RewardUser.user)
        .order_by(func.count(models.RewardUser.reward).desc())
        .first()
    )
    user, rewards = rewardest
    user = db.query(models.User).filter(models.User.id == user).first()
    return user, rewards


def get_user_with_max_scores(db: Session):
    max_scores = (
        db.query(models.RewardUser.user, func.sum(models.Reward.score))
        .join(models.Reward, models.RewardUser.reward == models.Reward.id)
        .group_by(models.RewardUser.user)
        .order_by(func.sum(models.Reward.score).desc())
        .first()
    )
    user, scores = max_scores
    user = db.query(models.User).filter(models.User.id == user).first()
    return user, scores


def get_user_with_min_scores(db: Session):
    min_scores = (
        db.query(models.RewardUser.user, func.sum(models.Reward.score))
        .join(models.Reward, models.RewardUser.reward == models.Reward.id)
        .group_by(models.RewardUser.user)
        .order_by(func.sum(models.Reward.score).asc())
        .first()
    )
    user, scores = min_scores
    user = db.query(models.User).filter(models.User.id == user).first()
    return user, scores


def get_users_with_most_difference(db: Session):
    user_max, score_max = get_user_with_max_scores(db)
    user_min, score_min = get_user_with_min_scores(db)
    difference = score_max - score_min
    return user_max, score_max, user_min, score_min, difference


def get_users_with_less_difference(db: Session):
    users = (
        db.query(models.RewardUser.user, func.sum(models.Reward.score))
        .join(models.Reward, models.RewardUser.reward == models.Reward.id)
        .group_by(models.RewardUser.user)
        .order_by(func.sum(models.Reward.score).desc())
        .limit(2)
    )
    first_user, first_user_scores = users.first()
    second_user, second_user_scores = users.offset(1).first()
    difference = first_user_scores - second_user_scores
    first_user = (
        db.query(models.User).filter(models.User.id == first_user).first()
    )
    second_user = (
        db.query(models.User).filter(models.User.id == second_user).first()
    )
    return (
        first_user,
        first_user_scores,
        second_user,
        second_user_scores,
        difference
    )


def get_users_rewarded_for_week(db: Session):
    query = (
        db.query(
            models.RewardUser.user,
            func.array_agg(func.DATE(models.RewardUser.gave_at).distinct())
        )
        .group_by(models.RewardUser.user)
        .all()
    )
    users = []
    for user, dates in query:
        count = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i-1] != timedelta(days=1):
                count = 1
            else:
                count += 1
            if count == 7:
                break
        if count >= 7:
            user = db.query(models.User).filter(models.User.id == user).first()
            users.append(user)
    return users


def get_user_rewards(db: Session, id: int):
    query = (
        db.query(models.Reward)
        .join(models.RewardUser, models.RewardUser.reward == models.Reward.id)
        .filter(models.RewardUser.user == id).all()
    )
    lang = db.query(models.User.language).filter(models.User.id == id).first()
    for i in query:
        i.title = mtranslate.translate(i.title, lang[0])
        i.description = mtranslate.translate(i.description, lang[0])
    return query
