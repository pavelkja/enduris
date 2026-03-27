from sqlalchemy.dialects.postgresql import insert

from app.core.database import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.models.activity_metric import ActivityMetric

from app.metrics.intensity import compute_avg_hr_percent

from app.services.stream_loader import load_streams
from app.services.metrics_engine import compute_metrics


def main():

    db = SessionLocal()

    user = db.query(User).first()

    activities = db.query(Activity).all()

    print("Activities:", len(activities))

    for activity in activities:

        print(f"\nProcessing activity: {activity.id}")

        # načtení streams z databáze
        streams = load_streams(db, activity.id)

        if not streams:
            print("No streams → skipping")
            continue

        print("Streams keys:", streams.keys())

        # výpočet metrik ze streams engine
        results = compute_metrics(activity, streams)

        print("Engine metrics:", results)

        # ---------------------------------------
        # avg_hr_percent (simple intensity metric)
        # ---------------------------------------

        avg_hr_percent = compute_avg_hr_percent(activity, user)

        if avg_hr_percent is not None:
            results.append({
                "metric_name": "avg_hr_percent",
                "value": avg_hr_percent
            })

        # ---------------------------------------

        for result in results:

            stmt = insert(ActivityMetric).values(
                activity_id=activity.id,
                user_id=user.id,
                metric_name=result["metric_name"],
                value=result["value"]
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=["activity_id", "metric_name"],
                set_={"value": result["value"]}
            )

            db.execute(stmt)

    db.commit()

    print("Metrics computed")


if __name__ == "__main__":
    main()