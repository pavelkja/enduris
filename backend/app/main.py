from fastapi import FastAPI

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