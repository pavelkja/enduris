from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.trends import get_efficiency_trend_with_insight
from app.services.performance import get_performance_summary
from app.services.readiness import ReadinessService

from app.repositories.metrics_repository import MetricsRepository
from app.schemas.performance import PerformanceSummary


router = APIRouter()

@router.get("/insight/deviation")
def get_efficiency_deviation_insight(
    user_id: str,
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT am.value AS efficiency
        FROM activity_metrics am
        JOIN activities a ON a.id = am.activity_id
        WHERE am.user_id = :user_id
          AND am.metric_name = 'efficiency'
        ORDER BY a.start_date DESC
        LIMIT 11;
    """)

    rows = db.execute(query, {"user_id": user_id}).fetchall()
    values = [float(row.efficiency) for row in rows if row.efficiency is not None]

    if len(values) < 2:
        return {
            "state": "normal",
            "today": values[0] if values else 0.0,
            "baseline": values[0] if values else 0.0,
            "deviation": 0.0,
        }

    today_value = values[0]
    baseline_values = values[1:11]
    baseline_avg = sum(baseline_values) / len(baseline_values)

    if baseline_avg == 0:
        deviation = 0.0
    else:
        deviation = (today_value - baseline_avg) / baseline_avg

    if deviation > 0.05:
        state = "above"
    elif deviation < -0.05:
        state = "below"
    else:
        state = "normal"

    return {
        "state": state,
        "today": today_value,
        "baseline": baseline_avg,
        "deviation": deviation,
    }



# 🔹 READINESS
@router.get("/dashboard/readiness")
def get_readiness(
    user_id: str,
    sport_type: str,
    db: Session = Depends(get_db)
):
    repo = MetricsRepository(db)
    service = ReadinessService(repo)

    return service.get_readiness(
        user_id=user_id,
        sport_type=sport_type
    )


# 🔹 TIME-BASED TREND (daily_metrics)
@router.get("/dashboard/health")
def get_health_dashboard(
    user_id: str,
    sport_type: str,
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            date,
            efficiency_avg,

            AVG(efficiency_avg) OVER (
                ORDER BY date
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ) as efficiency_7d,

            AVG(efficiency_avg) OVER (
                ORDER BY date
                ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
            ) as efficiency_14d

        FROM daily_metrics
        WHERE user_id = :user_id
          AND sport_type = :sport_type
        ORDER BY date;
    """)

    result = db.execute(query, {
        "user_id": user_id,
        "sport_type": sport_type
    })

    data = [
        {
            "date": row.date,
            "efficiency": row.efficiency_avg,
            "efficiency_7d": row.efficiency_7d,
            "efficiency_14d": row.efficiency_14d,
        }
        for row in result
    ]

    return data


# 🔥 ACTIVITY-BASED TREND
@router.get("/dashboard/efficiency-trend")
def efficiency_trend(user_id: str, sport_type: str):
    return get_efficiency_trend_with_insight(user_id, sport_type)


# 🔹 SPORT TYPES
@router.get("/dashboard/sport-types")
def get_sport_types(user_id: str, db: Session = Depends(get_db)):

    query = text("""
        SELECT DISTINCT sport_type
        FROM activities
        WHERE user_id = :user_id
        ORDER BY sport_type;
    """)

    result = db.execute(query, {"user_id": user_id})

    return [row.sport_type for row in result]


# 🔹 PERFORMANCE SUMMARY
@router.get("/dashboard/performance-summary", response_model=PerformanceSummary)
def performance_summary(
    user_id: str,
    sport_type: str,
    db: Session = Depends(get_db)
):
    return get_performance_summary(db, user_id, sport_type)
