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
