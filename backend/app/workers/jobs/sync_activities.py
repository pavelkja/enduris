from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.services.strava_client import get_athlete_activities


def sync_activities_job(user_id: str):
    print(f"Starting sync... user_id={user_id}")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            print(f"User not found: {user_id}")
            return

        if not user.access_token:
            print(f"Missing access token for user: {user_id}")
            return

        activities = get_athlete_activities(
            access_token=user.access_token,
            page=1,
            per_page=30,
        )

        print(f"Fetched {len(activities)} activities")

        saved_count = 0

        for act in activities:
            activity_id = act.get("id")
            if activity_id is None:
                continue

            exists = db.query(Activity).filter(Activity.id == activity_id).first()
            if exists:
                continue

            start_date_raw = act.get("start_date")
            if not start_date_raw:
                continue

            start_date = datetime.fromisoformat(start_date_raw.replace("Z", "+00:00"))
            if start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=timezone.utc)

            sport_type = act.get("sport_type")
            if not sport_type:
                continue

            activity = Activity(
                id=activity_id,
                user_id=user.id,
                sport_type=sport_type,
                start_date=start_date,
                distance=act.get("distance"),
                moving_time=act.get("moving_time"),
                elapsed_time=act.get("elapsed_time"),
                elevation_gain=act.get("total_elevation_gain"),
                avg_speed=act.get("average_speed"),
                max_speed=act.get("max_speed"),
                avg_hr=act.get("average_heartrate"),
                max_hr=act.get("max_heartrate"),
                has_heartrate=bool(
                    act.get("has_heartrate") or act.get("average_heartrate")
                ),
            )

            db.add(activity)
            saved_count += 1

        db.commit()
        print(f"Saved {saved_count} activities")

    finally:
        db.close()
