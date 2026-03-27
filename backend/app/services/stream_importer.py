import requests
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_stream import ActivityStream
from app.models.user import User

from app.services.metrics_engine import compute_metrics
from app.services.strava_client import refresh_access_token


STRAVA_API = "https://www.strava.com/api/v3"


STREAM_KEYS = "time,heartrate,altitude,latlng,cadence,distance"


# 🔥 FETCH STREAMS
def fetch_streams(db: Session, user: User, activity_id):

    url = f"{STRAVA_API}/activities/{activity_id}/streams"

    params = {
        "keys": STREAM_KEYS,
        "key_by_type": "true"
    }

    headers = {
        "Authorization": f"Bearer {user.access_token}"
    }

    response = requests.get(url, headers=headers, params=params, timeout=(5, 30))

    # 🔥 401 → refresh token
    if response.status_code == 401:
        print(f"🔑 Token expired for {activity_id}")

        new_token = refresh_access_token(user, db)

        if not new_token:
            return None

        headers["Authorization"] = f"Bearer {new_token}"
        response = requests.get(url, headers=headers, params=params, timeout=(5, 30))

    # 🔥 RATE LIMIT → STOP
    if response.status_code == 429:
        print(f"⏳ Rate limit hit for {activity_id}")
        return "RATE_LIMIT"

    if response.status_code != 200:
        print("❌ Stream fetch failed:", activity_id, response.status_code)
        return None

    return response.json()


# 🔥 MAIN IMPORT
def import_streams(db: Session, user: User, activity: Activity):

    # 🔹 už existují?
    existing = db.query(ActivityStream).filter(
        ActivityStream.activity_id == activity.id
    ).first()

    if existing:
        print("⚠️ Streams already exist:", activity.id)
        activity.streams_imported = True
        db.commit()
        return

    # 🔹 fetch
    streams = fetch_streams(db, user, activity.id)

    # 🔥 STOP celý batch
    if streams == "RATE_LIMIT":
        return "STOP"

    if streams is None:
        print("❌ No streams:", activity.id)
        return

    # 🔹 uložit streams
    saved_any = False

    for stream_type, stream_data in streams.items():

        data = stream_data.get("data")

        if not data:
            continue

        stream = ActivityStream(
            activity_id=activity.id,
            user_id=user.id,
            stream_type=stream_type,
            data=data
        )

        db.add(stream)
        saved_any = True

    if not saved_any:
        print("❌ Empty streams:", activity.id)
        return

    db.commit()
    print("✅ Streams imported:", activity.id)

    # 🔥 metrics
    try:
        compute_metrics(db, activity, streams)
        print("📊 Metrics computed:", activity.id)
    except Exception as e:
        print(f"❌ Metrics failed for {activity.id}: {e}")
        db.rollback()
        return

    # 🔹 označit až na konci
    activity.streams_imported = True
    db.commit()

    print("🏁 Activity fully processed:", activity.id)
