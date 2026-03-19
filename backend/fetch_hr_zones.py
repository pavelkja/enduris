import requests

from app.core.database import SessionLocal
from app.models.user import User
from app.models.activity import Activity


STRAVA_API = "https://www.strava.com/api/v3"


def main():

    db = SessionLocal()

    user = db.query(User).first()

    headers = {
        "Authorization": f"Bearer {user.access_token}"
    }

    response = requests.get(
        f"{STRAVA_API}/athlete",
        headers=headers
    )

    data = response.json()

    zones = data.get("heart_rate_zones")

    print("HR zones:", zones)

    user.hr_zones = zones

    db.commit()


if __name__ == "__main__":
    main()