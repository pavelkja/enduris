from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.user import User
from app.models.activity import Activity
from app.services.strava_client import get_athlete_activities


SUPPORTED_SPORTS = {
    "Ride",
    "MountainBikeRide",
    "GravelRide",
    "VirtualRide",
    "Run",
    "TrailRun",
    "VirtualRun"
}


def import_activities(db: Session, user_id, access_token: str):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception(f"User {user_id} not found")

    page = 1
    per_page = 30
    total_imported = 0

    # připravíme timestamp pro incremental sync
    after_timestamp = None

    if user.last_sync:
        after_timestamp = int(user.last_sync.timestamp())
        print(f"Incremental sync after {after_timestamp}")
    else:
        print("Initial full sync")

    while True:

        print(f"Fetching page {page}")

        activities = get_athlete_activities(
            access_token,
            page=page,
            per_page=per_page,
            after=after_timestamp
        )

        # konec pagination
        if not activities:
            print("No more activities found.")
            break

        # optimalizace incremental sync
        if after_timestamp and len(activities) < per_page:
            print("Last page of incremental sync reached.")
            break

        print(f"Activities received: {len(activities)}")

        for act in activities:

            # filtrovat sporty
            if act.get("sport_type") not in SUPPORTED_SPORTS:
                continue

            # filtrovat aktivity bez HR
            if not act.get("has_heartrate"):
                continue

            activity = Activity(
                id=act["id"],
                user_id=user_id,
                sport_type=act.get("sport_type"),
                start_date=act.get("start_date"),
                distance=act.get("distance"),
                moving_time=act.get("moving_time"),
                elapsed_time=act.get("elapsed_time"),
                elevation_gain=act.get("total_elevation_gain"),
                avg_speed=act.get("average_speed"),
                max_speed=act.get("max_speed"),
                avg_hr=act.get("average_heartrate"),
                max_hr=act.get("max_heartrate")
            )

            db.merge(activity)

            total_imported += 1

        db.commit()

        print(f"Page {page} processed")

        page += 1

    # uložíme čas posledního syncu až po dokončení
    user.last_sync = datetime.now(timezone.utc)
    db.commit()

    print(f"Total imported: {total_imported}")

    return total_imported