from typing import Optional

from sqlalchemy import case, func, text
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.activity_metric import ActivityMetric

class MetricsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_last_activities_with_metrics(self, user_id: str, sport_type: str, limit: int = 7):
        efficiency = func.max(
            case(
                (ActivityMetric.metric_name == "efficiency", ActivityMetric.value),
            )
        ).label("efficiency")

        hr_drift = func.max(
            case(
                (ActivityMetric.metric_name == "hr_drift", ActivityMetric.value),
            )
        ).label("hr_drift")

        rows = (
            self.db.query(
                Activity.id.label("id"),
                Activity.start_date.label("start_date"),
                efficiency,
                hr_drift,
            )
            .outerjoin(ActivityMetric, Activity.id == ActivityMetric.activity_id)
            .filter(Activity.user_id == user_id)
            .filter(func.lower(func.trim(Activity.sport_type)) == func.lower(func.trim(sport_type)))
            .group_by(Activity.id, Activity.start_date)
            .order_by(Activity.start_date.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": row.id,
                "start_date": row.start_date,
                "efficiency": None if row.efficiency is None else float(row.efficiency),
                "hr_drift": None if row.hr_drift is None else float(row.hr_drift),
            }
            for row in rows
        ]

    def get_latest_activity_date(self, user_id: str, sport_type: Optional[str] = None):
        query = self.db.query(func.max(Activity.start_date).label("latest_date")).filter(
            Activity.user_id == user_id
        )

        if sport_type:
            query = query.filter(Activity.sport_type == sport_type)

        result = query.one_or_none()

        return result.latest_date if result and result.latest_date else None

        result = self.db.execute(query, params).fetchone()

        return result.latest_date if result and result.latest_date else None
