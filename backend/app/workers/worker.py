from rq import Connection, Worker

from app.workers.redis import get_redis_connection


def run_worker() -> None:
    connection = get_redis_connection()
    with Connection(connection):
        worker = Worker(["default"])
        worker.work(with_scheduler=True)


if __name__ == "__main__":
    run_worker()
