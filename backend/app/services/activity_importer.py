from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import os

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

INCREMENTAL_LOOKBACK_DAYS = int(os.getenv("STRAVA_INCREMENTAL_LOOKBACK_DAYS", "30"))


def import_activities(db: Session, user_id):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception(f"User {user_id} not found")

    page = 1
    per_page = 30
    total_imported = 0
    total_fetched = 0

    # držíme nejnovější start_date napříč všemi stránkami,
    # aby se checkpoint nastavil přesně na poslední aktivitu ze Stravy
    newest_activity_start_date = None

    # připravíme timestamp pro incremental sync
    after_timestamp = None

    if user.last_sync:
        # Použijeme překryvné okno, aby se doimportovaly i později upravené
        # nebo se zpožděním zpracované aktivity.
        overlap_window = timedelta(days=INCREMENTAL_LOOKBACK_DAYS)
        incremental_from = user.last_sync - overlap_window
        after_timestamp = int(incremental_from.timestamp())
        print(f"Incremental sync after {after_timestamp}")
    else:
        print("Initial full sync")

    while True:

        print(f"Fetching page {page}")

        activities = get_athlete_activities(
            user.access_token,
            page=page,
            per_page=per_page,
            after=after_timestamp,
            db=db,
            user=user
        )

        # konec pagination
        if not activities:
            print("No more activities found.")
            break

        total_fetched += len(activities)
        
        print(f"Activities received: {len(activities)}")

        for act in activities:
            start_date_raw = act.get("start_date")
            start_date = None

            if isinstance(start_date_raw, str):
                # Strava vrací UTC ISO string, nejčastěji se suffixem "Z"
                # fromisoformat neumí přímo "Z", proto převod na +00:00
                start_date = datetime.fromisoformat(start_date_raw.replace("Z", "+00:00"))
                if start_date.tzinfo is None:
                    start_date = start_date.replace(tzinfo=timezone.utc)

                if newest_activity_start_date is None or start_date > newest_activity_start_date:
                    newest_activity_start_date = start_date

            # filtrovat sporty
            if act.get("sport_type") not in SUPPORTED_SPORTS:
                continue

            # filtrovat aktivity bez HR
            if not act.get("has_heartrate"):
                continue

            if start_date is None:
                # Aktivita bez validního start_date nesmí spadnout celý import,
                # pouze ji přeskočíme.
                print(f"Skipping activity {act.get('id')} due to missing or invalid start_date")
                continue


            activity = Activity(
                id=act["id"],
                user_id=user_id,
                sport_type=act.get("sport_type"),
                start_date=start_date,
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

        # incremental sync: poslední stránka je kratší než per_page
        if after_timestamp and len(activities) < per_page:
            print("Last page of incremental sync reached.")
            break


        page += 1

    # Posouváme checkpoint pouze pokud Strava skutečně vrátila nějaké aktivity
    # s validním start_date napříč všemi stránkami.
    if newest_activity_start_date is not None:
        user.last_sync = newest_activity_start_date
        db.commit()
    else:
        print("No activities fetched from Strava; keeping previous last_sync.")

    print(f"Total imported: {total_imported}")

    return total_imported
