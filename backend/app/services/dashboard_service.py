from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.activity_metric import ActivityMetric


def get_efficiency_trend(db: Session, user_id: str, limit: int = 30):
    """
    Vrátí posledních N aktivit s metrikou efficiency
    """

    results = (
        db.query(
            Activity.id,
            Activity.start_date,
            ActivityMetric.value.label("efficiency")
        )
        .join(
            ActivityMetric,
            Activity.id == ActivityMetric.activity_id
        )
        .filter(
            Activity.user_id == user_id,
            ActivityMetric.metric_name == "efficiency"
        )
        .order_by(Activity.start_date.desc())
        .limit(limit)
        .all()
    )

    # převedeme do listu dictů
    data = [
        {
            "activity_id": r.id,
            "date": r.start_date,
            "efficiency": r.efficiency
        }
        for r in results
    ]

    # otočíme, aby to šlo od nejstarší → nejnovější
    data.reverse()

    return data

def compute_trend(data):
    if len(data) < 5:
        return "not_enough_data"

    last_5 = data[-5:]
    prev_5 = data[-10:-5]

    if len(prev_5) < 5:
        return "not_enough_data"

    last_avg = sum(d["efficiency"] for d in last_5) / 5
    prev_avg = sum(d["efficiency"] for d in prev_5) / 5

    diff = last_avg - prev_avg

    # threshold proti šumu
    if abs(diff) < 0.002:
        return "stable"
    elif diff > 0:
        return "improving"
    else:
        return "declining"
