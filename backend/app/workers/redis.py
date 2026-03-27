import os
from redis import Redis

_redis_conn = None

def get_redis_connection() -> Redis:
    global _redis_conn

    if _redis_conn is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _redis_conn = Redis.from_url(redis_url)

    return _redis_conn
