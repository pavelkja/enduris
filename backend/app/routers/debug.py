from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.models.activity import Activity
from app.models.activity_stream import ActivityStream
from app.models.user import User
from app.services.metrics_engine import compute_metrics
from app.services.stream_importer import fetch_streams

router = APIRouter(prefix="/api/debug", tags=["debug"])


def fetch_streams_for_activity(activity: Activity, db: Session):
    user = db.query(User).filter(User.id == activity.user_id).first()

    if not user:
        print(f"[debug-recompute] User not found for activity {activity.id}")
        return None

    print(f"[debug-recompute] Fetching streams for activity {activity.id}")
    streams = fetch_streams(db=db, user=user, activity_id=activity.id)

    if streams == "RATE_LIMIT":
        print(f"[debug-recompute] Strava rate limit hit at activity {activity.id}")
        return "RATE_LIMIT"

    if not streams:
        print(f"[debug-recompute] No streams returned for activity {activity.id}")
        return None

    db.query(ActivityStream).filter(
        ActivityStream.activity_id == activity.id
    ).delete(synchronize_session=False)

    saved_count = 0

    for stream_type, stream_payload in streams.items():
        stream_data = (
            stream_payload.get("data")
            if isinstance(stream_payload, dict)
            else stream_payload
        )

        if not stream_data:
            continue

        db.add(
            ActivityStream(
                activity_id=activity.id,
                user_id=activity.user_id,
                stream_type=stream_type,
                data=stream_data,
            )
        )
        saved_count += 1

    activity.streams_imported = saved_count > 0
    db.commit()

    print(
        f"[debug-recompute] Saved {saved_count} stream(s) "
        f"for activity {activity.id}"
    )

    return streams


def compute_metrics_for_activity(activity: Activity, streams, db: Session):
    print(f"[debug-recompute] Recomputing metrics for activity {activity.id}")
    compute_metrics(db=db, activity=activity, streams=streams)
    print(f"[debug-recompute] Metrics recomputed for activity {activity.id}")


def recompute_user_activities(user_id: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            print(f"[debug-recompute] User not found: {user_id}")
            return

        activities = (
            db.query(Activity)
            .filter(Activity.user_id == user.id)
            .order_by(Activity.start_date.desc())
            .all()
        )

        total = len(activities)
        print(
            f"[debug-recompute] Starting brute force recompute for user {user_id}; "
            f"activities={total}"
        )

        for index, activity in enumerate(activities, start=1):
            print(
                f"[debug-recompute] Processing activity "
                f"{index}/{total}: {activity.id}"
            )

            try:
                streams = fetch_streams_for_activity(activity=activity, db=db)

                if streams == "RATE_LIMIT":
                    print("[debug-recompute] Stopping due to Strava rate limit")
                    break

                if not streams:
                    continue

                compute_metrics_for_activity(
                    activity=activity,
                    streams=streams,
                    db=db,
                )
            except Exception as exc:
                db.rollback()
                print(f"[debug-recompute] Failed activity {activity.id}: {exc}")

        print(f"[debug-recompute] Finished brute force recompute for user {user_id}")
    finally:
        db.close()


@router.post("/users/{user_id}/recompute-activities")
def recompute_activities_for_user(
    user_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user_exists = db.query(User.id).filter(User.id == user_id).first()

    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    background_tasks.add_task(recompute_user_activities, user_id)

    return {
        "status": "started",
        "user_id": user_id,
        "message": "Brute force activity stream fetch and metric recompute queued",
    }
