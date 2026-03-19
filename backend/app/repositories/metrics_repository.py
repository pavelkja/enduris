from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional


class MetricsRepository:
    def __init__(self, db: Session):
                self.db = db

    def get_last_activities_with_metrics(self, user_id: str, sport_type: str, limit: int = 7):
        query = text("""
            SELECT 
              a.id as activity_id,
              a.start_date,
                        MAX(CASE WHEN m.metric_name = 'efficiency' THEN m.value END) as efficiency,
                        MAX(CASE WHEN m.metric_name = 'hr_drift' THEN m.value END) as hr_drift
                    FROM activities a
                    LEFT JOIN activity_metrics m 
                        ON a.id = m.activity_id
                        AND m.metric_name IN ('efficiency', 'hr_drift')
                    WHERE a.user_id = :user_id
                      AND LOWER(TRIM(a.sport_type)) = LOWER(TRIM(:sport_type))
                    GROUP BY a.id, a.start_date
                    ORDER BY a.start_date DESC
                    LIMIT :limit
                """)

        result = self.db.execute(query, {
                    "user_id": user_id,
                    "sport_type": sport_type,
                    "limit": limit
                })

        return [dict(row._mapping) for row in result]

    def get_latest_activity_date(self, user_id: str, sport_type: Optional[str] = None):
                query = text("""
                    SELECT MAX(start_date) as latest_date
                    FROM activities
                    WHERE user_id = :user_id
                    {sport_filter}
                """.format(
                    sport_filter="AND sport_type = :sport_type" if sport_type else ""
                ))

                params = {"user_id": user_id}
                if sport_type:
                    params["sport_type"] = sport_type

                result = self.db.execute(query, params).fetchone()

                return result.latest_date if result and result.latest_date else None