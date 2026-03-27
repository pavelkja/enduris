from rq import Queue

from app.workers.redis import get_redis_connection


def get_default_queue() -> Queue:
    return Queue("default", connection=get_redis_connection())
