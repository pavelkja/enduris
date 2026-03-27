from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models.user import User

app = FastAPI()


@app.on_event("startup")
def startup():
    print("CREATING DATABASE TABLES")
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/dev/create-test-user")
def create_test_user(db: Session = Depends(get_db)):

    user = User(
        strava_athlete_id=123456,
        name="Test Rider",
        email="test@enduris.app"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    }