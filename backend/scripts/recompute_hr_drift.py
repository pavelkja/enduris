from app.core.database import SessionLocal
from sqlalchemy import text

from app.metrics import hr_drift


def main():
    db = SessionLocal()

    # vezmeme aktivity, které mají streamy
    activities = db.execute(text("""
        SELECT DISTINCT activity_id
        FROM activity_streams
    """)).fetchall()

    print(f"Found {len(activities)} activities")

    for row in activities:
        activity_id = row.activity_id

        # načti streamy
        streams_rows = db.execute(text("""
            SELECT stream_type, data
            FROM activity_streams
            WHERE activity_id = :activity_id
        """), {"activity_id": activity_id}).fetchall()

        streams = {
            r.stream_type: {"data": r.data}
            for r in streams_rows
        }

        result = hr_drift.compute(None, streams)

        if result is None:
            continue

        # UPSERT (jednoduchá varianta: delete + insert)
        db.execute(text("""
            DELETE FROM activity_metrics
            WHERE activity_id = :activity_id
              AND metric_name = 'hr_drift'
        """), {"activity_id": activity_id})

        db.execute(text("""
            INSERT INTO activity_metrics (activity_id, metric_name, value)
            VALUES (:activity_id, :metric_name, :value)
        """), {
            "activity_id": activity_id,
            "metric_name": result["metric_name"],
            "value": result["value"]
        })

    db.commit()
    db.close()

    print("DONE")


if __name__ == "__main__":
    main()