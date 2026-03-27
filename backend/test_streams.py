import requests
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.models.activity import Activity


STRAVA_API = "https://www.strava.com/api/v3"


def get_first_activity(db: Session):
    return db.query(Activity).first()


def get_user(db: Session):
    return db.query(User).first()


def fetch_streams(access_token, activity_id):

    url = f"{STRAVA_API}/activities/{activity_id}/streams"

    params = {
        "keys": "time,heartrate,speed,altitude,grade,cadence,latlng",
        "key_by_type": "true"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers, params=params)

    print("STATUS:", response.status_code)

    data = response.json()

    print("STREAM TYPES:")
    for key in data.keys():
        print("-", key)

    if "heartrate" in data:
        print("HR SAMPLE:", data["heartrate"]["data"][:10])


def main():

    db = SessionLocal()

    user = get_user(db)
    activity = get_first_activity(db)

    print("Testing activity:", activity.id)

    fetch_streams(user.access_token, activity.id)


if __name__ == "__main__":
    main()