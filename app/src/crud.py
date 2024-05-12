from datetime import timedelta

import mtranslate
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import Reward, RewardUser, User
from src.schemas import RewardAdd, RewardUserAdd, UserAdd


def add_user(db: Session, user: UserAdd):
    user = User(
        name=user.name,
        language=user.language
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, id: int):
    user = db.query(User).filter_by(id=id).first()
    return user


def add_reward(db: Session, reward: RewardAdd):
    reward = Reward(
        title=reward.title,
        score=reward.score,
        description=reward.description
    )
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def get_reward(db: Session, id: int):
    reward = db.query(Reward).filter_by(id=id).first()
    return reward


def reward_user(db: Session, rewarding: RewardUserAdd):
    rewarding = RewardUser(
        user=rewarding.user,
        reward=rewarding.reward
    )
    db.add(rewarding)
    db.commit()
    db.refresh(rewarding)
    return rewarding


def get_rewardest_user(db: Session):
    rewardest = (
        db.query(RewardUser.user, func.count(RewardUser.reward))
        .group_by(RewardUser.user)
        .order_by(func.count(RewardUser.reward).desc())
        .first()
    )
    user, rewards = rewardest
    user = db.query(User).filter_by(id=user).first()
    result = {'user': user, 'rewards': rewards}
    return result


def get_user_with_max_scores(db: Session):
    max_scores = (
        db.query(RewardUser.user, func.sum(Reward.score))
        .join(Reward, RewardUser.reward == Reward.id)
        .group_by(RewardUser.user)
        .order_by(func.sum(Reward.score).desc())
        .first()
    )
    user, scores = max_scores
    user = db.query(User).filter_by(id=user).first()
    result = {'user': user, 'scores': scores}
    return result


def get_user_with_min_scores(db: Session):
    min_scores = (
        db.query(RewardUser.user, func.sum(Reward.score))
        .join(Reward, RewardUser.reward == Reward.id)
        .group_by(RewardUser.user)
        .order_by(func.sum(Reward.score).asc())
        .first()
    )
    user, scores = min_scores
    user = db.query(User).filter_by(id=user).first()
    result = {'user': user, 'scores': scores}
    return result


def get_users_with_most_difference(db: Session):
    max_user = get_user_with_max_scores(db)
    min_user = get_user_with_min_scores(db)
    difference = max_user['scores'] - min_user['scores']
    max_user['max_user'] = max_user.pop('user')
    max_user['max_scores'] = max_user.pop('scores')
    min_user['min_user'] = min_user.pop('user')
    min_user['min_scores'] = min_user.pop('scores')
    result = {**max_user, **min_user}
    result['difference'] = difference
    return result


def get_users_with_less_difference(db: Session):
    users = (
        db.query(RewardUser.user, func.sum(Reward.score))
        .join(Reward, RewardUser.reward == Reward.id)
        .group_by(RewardUser.user)
        .order_by(func.sum(Reward.score).desc())
        .limit(2)
    )
    first_user, first_user_scores = users.first()
    second_user, second_user_scores = users.offset(1).first()
    difference = first_user_scores - second_user_scores
    first_user = (db.query(User).filter_by(id=first_user).first())
    second_user = (db.query(User).filter_by(id=second_user).first())
    result = {
        'first_user': first_user,
        'first_user_scores': first_user_scores,
        'second_user': second_user,
        'second_user_scores': second_user_scores,
        'difference': difference
    }
    return result


def get_users_rewarded_for_week(db: Session):
    query = (
        db.query(
            RewardUser.user,
            func.array_agg(func.DATE(RewardUser.gave_at).distinct())
        )
        .group_by(RewardUser.user)
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
            user = db.query(User).filter_by(id=user).first()
            users.append(user)
    return users


def get_user_rewards(db: Session, id: int):
    rewards = (
        db.query(Reward)
        .join(RewardUser, RewardUser.reward == Reward.id)
        .filter(RewardUser.user == id).all()
    )
    language = db.query(User.language).filter_by(id=id).first()
    for reward in rewards:
        reward.title = mtranslate.translate(reward.title, language[0])
        reward.description = mtranslate.translate(
            reward.description, language[0]
        )
    return rewards
