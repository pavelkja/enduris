from sqlalchemy.orm import Session
from app.models.activity_stream import ActivityStream


def load_streams(db: Session, activity_id):

    rows = (
        db.query(ActivityStream)
        .filter(ActivityStream.activity_id == activity_id)
        .all()
    )

    streams = {}

    for row in rows:
        streams[row.stream_type] = row.data

    return streams