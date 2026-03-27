from app.metrics import efficiency
from app.metrics import hr_drift
from app.metrics import aerobic_decoupling

from app.models.activity_metric import ActivityMetric


METRICS = [
    efficiency,
    hr_drift,
    aerobic_decoupling
]


def compute_metrics(db, activity, streams):

    print(f"\n📊 Computing metrics for activity {activity.id}")

    computed_any = False

    for metric in METRICS:

        try:
            result = metric.compute(activity, streams)

            print(f"DEBUG {metric.__name__} → {result}")

            if result is None:
                continue

            metric_name = result["metric_name"]
            value = result["value"]

            # 🔹 UPSERT
            existing = db.query(ActivityMetric).filter(
                ActivityMetric.activity_id == activity.id,
                ActivityMetric.metric_name == metric_name
            ).first()

            if existing:
                existing.value = value
                print(f"↻ Updated {metric_name}: {value}")
            else:
                new_metric = ActivityMetric(
                    activity_id=activity.id,
                    user_id=activity.user_id,
                    metric_name=metric_name,
                    value=value
                )
                db.add(new_metric)
                print(f"➕ Created {metric_name}: {value}")

            computed_any = True

        except Exception as e:
            print(f"❌ ERROR in {metric.__name__}: {e}")

    if computed_any:
        activity.metrics_computed = True
        print("✅ Metrics stored")
    else:
        print("⚠️ No metrics computed")

    db.commit()