from api.constants import REDIS_USER_KEY


def get_redis_user_key(user_id: str):
    return f"{REDIS_USER_KEY}:{user_id}"
