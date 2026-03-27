from rq import Queue
from app.workers.redis import get_redis_connection

_queue = None

def get_default_queue() -> Queue:
    global _queue

    if _queue is None:
        _queue = Queue("default", connection=get_redis_connection())

    return _queue
