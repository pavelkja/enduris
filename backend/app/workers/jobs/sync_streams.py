from time import sleep

from app.core.database import SessionLocal
from app.models.activity import Activity
from app.models.activity_stream import ActivityStream
from app.models.user import User
from app.services.strava_client import get_activity_streams


STREAM_TYPES = ["heartrate", "speed", "altitude", "cadence"]


def sync_streams_job(user_id: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            print(f"User not found: {user_id}")
            return

        activities = (
            db.query(Activity)
            .filter(
                Activity.user_id == user.id,
                Activity.streams_imported == False,
            )
            .order_by(Activity.start_date.desc())
            .limit(10)
            .all()
        )

        for activity in activities:
            print(f"Processing activity {activity.id}")

            existing = (
                db.query(ActivityStream)
                .filter(ActivityStream.activity_id == activity.id)
                .first()
            )

            if existing:
                print("Streams already exist")
                activity.streams_imported = True
                db.commit()
                continue

            streams = get_activity_streams(
                activity_id=activity.id,
                access_token=user.access_token,
                db=db,
                user=user,
            )

            if not streams:
                continue

            saved_any = False

            for stream_type in STREAM_TYPES:
                stream_values = streams.get(stream_type)

                if not stream_values:
                    continue

                db.add(
                    ActivityStream(
                        activity_id=activity.id,
                        user_id=user.id,
                        stream_type=stream_type,
                        data=stream_values,
                    )
                )
                saved_any = True

            if saved_any:
                activity.streams_imported = True
                db.commit()
                print("Streams saved")
            else:
                print("No streams to save")

            sleep(0.3)

    finally:
        db.close()
