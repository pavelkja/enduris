from fastapi import FastAPI

from app.workers.jobs.test_job import test_job
from app.workers.jobs.sync_activities import sync_activities_job
from app.workers.queue import get_default_queue

from app.core.database import Base, engine

from app.models.user import User
from app.models.activity import Activity
from app.models.activity_stream import ActivityStream
from app.models.activity_metric import ActivityMetric

from app.api.dashboard import router as dashboard_router
from app.routers import health

app = FastAPI(
    title="Enduris API",
    version="0.1"
)

app.include_router(dashboard_router, prefix="/api")

# vytvoření tabulek v databázi
Base.metadata.create_all(bind=engine)

# registrace routerů
app.include_router(health.router)


@app.get("/")
def root():
    return {"status": "Enduris backend running"}


@app.post("/api/test-job")
def enqueue_test_job():
    queue = get_default_queue()
    job = queue.enqueue(test_job, 2, 3)
    return {"job_id": job.id}


@app.post("/api/sync")
def enqueue_sync_job(user_id: str):
    queue = get_default_queue()
    job = queue.enqueue(sync_activities_job, user_id)
    return {"job_id": job.id}
