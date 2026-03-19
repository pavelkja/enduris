from sqlalchemy import text
from app.core.database import engine
import statistics

from app.services.insights import generate_efficiency_insight


def get_efficiency_trend(user_id: str, sport_type: str = "Ride"):
    query = text("""
        SELECT
            a.start_date,
            m.value as efficiency,

            AVG(m.value) OVER (
                ORDER BY a.start_date
                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
            ) as efficiency_last_5,

            AVG(m.value) OVER (
                ORDER BY a.start_date
                ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
            ) as efficiency_last_10

        FROM activities a
        JOIN activity_metrics m 
            ON a.id = m.activity_id

        WHERE 
            a.user_id = :user_id
            AND m.metric_name = 'efficiency'
            AND a.sport_type = :sport_type

        ORDER BY a.start_date;
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "user_id": user_id,
            "sport_type": sport_type
        })

        return [
            {
                "date": row.start_date,
                "efficiency": row.efficiency,
                "efficiency_last_5": row.efficiency_last_5,
                "efficiency_last_10": row.efficiency_last_10,
            }
            for row in result
        ]


def interpret_efficiency_trend(data):
    if len(data) < 10:
        return "not_enough_data"

    latest = data[-1]

    last_5 = latest["efficiency_last_5"]
    last_10 = latest["efficiency_last_10"]

    if last_5 is None or last_10 is None:
        return "insufficient_data"

    diff = last_5 - last_10
    threshold = 0.002  # doladíme později

    if diff > threshold:
        return "improving"
    elif diff < -threshold:
        return "declining"
    else:
        return "stable"


def calculate_confidence(data):
    n = len(data)

    if n < 5:
        return "low"
    elif n < 10:
        return "medium"
    else:
        return "high"


def calculate_variability(data):
    values = [d["efficiency"] for d in data if d["efficiency"] is not None]

    if len(values) < 5:
        return "not_enough_data"

    std_dev = statistics.stdev(values)

    if std_dev < 0.003:
        return "very_stable"
    elif std_dev < 0.006:
        return "stable"
    else:
        return "volatile"


def get_efficiency_trend_with_insight(user_id: str, sport_type: str):
    data = get_efficiency_trend(user_id, sport_type)

    trend = interpret_efficiency_trend(data)
    confidence = calculate_confidence(data)
    variability = calculate_variability(data)

    insight = generate_efficiency_insight(
        trend=trend,
        confidence=confidence,
        variability=variability
    )

    return {
        "sport_type": sport_type,
        "trend": trend,
        "confidence": confidence,
        "variability": variability,
        "insight": insight,
        "data": data
    }