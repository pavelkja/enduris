from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User
from app.models.activity import Activity
from app.models.activity_stream import ActivityStream
from app.models.activity_metric import ActivityMetric

from app.api.dashboard import router as dashboard_router
from app.routers import health

# 🔽 RQ importy
# from app.workers.queue_config import queue
# from app.workers.jobs import test_job


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


# 🔽 TEST ENDPOINT PRO RQ
# @app.get("/test-job")
# def run_test_job():
  #  job = queue.enqueue(test_job)
  #  return {"job_id": job.id}
