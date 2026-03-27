from app.models.activity_stream import ActivityStream
from app.services.metrics_engine import compute_metrics


def compute_metrics_for_activity(db, activity):
    """
    Wrapper nad metrics_engine.
    Načte streams z DB a spustí výpočet metrik.
    """

    streams_rows = (
        db.query(ActivityStream)
        .filter(ActivityStream.activity_id == activity.id)
        .all()
    )

    if not streams_rows:
        print("No streams found for activity")
        return

    # 👉 převedeme DB → dict
    streams = {}

    for row in streams_rows:
        streams[row.stream_type] = row.data

    # 👉 zavoláme engine
    compute_metrics(db=db, activity=activity, streams=streams)

    # 👉 označíme jako spočítané
    activity.metrics_computed = True
    db.commit()

    print("Metrics computed (wrapper)")
