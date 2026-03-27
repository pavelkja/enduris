from rq import Worker
from app.workers.redis import get_redis_connection


def run_worker() -> None:
    connection = get_redis_connection()
    worker = Worker(["default"], connection=connection)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    run_worker()
