from sqlalchemy import text
from app.core.database import engine


def compute_daily_metrics(user_id: str):
    query = text("""
        WITH activity_agg AS (
            SELECT
                user_id,
                DATE(start_date) as date,
                SUM(distance) as distance,
                SUM(elevation_gain) as elevation
            FROM activities
            WHERE user_id = :user_id
            GROUP BY user_id, DATE(start_date)
        ),
        metrics_agg AS (
            SELECT
                a.user_id,
                DATE(a.start_date) as date,

                AVG(CASE WHEN m.metric_name = 'efficiency' THEN m.value END) as efficiency_avg,
                AVG(CASE WHEN m.metric_name = 'hr_drift' THEN m.value END) as hr_drift_avg,
                AVG(CASE WHEN m.metric_name = 'aerobic_decoupling' THEN m.value END) as aerobic_decoupling_avg,
                AVG(CASE WHEN m.metric_name = 'avg_hr_percent' THEN m.value END) as avg_hr_percent_avg

            FROM activities a
            LEFT JOIN activity_metrics m ON a.id = m.activity_id
            WHERE a.user_id = :user_id
            GROUP BY a.user_id, DATE(a.start_date)
        )

        INSERT INTO daily_metrics (
            user_id,
            date,
            distance,
            elevation,
            efficiency_avg,
            hr_drift_avg,
            aerobic_decoupling_avg,
            avg_hr_percent_avg
        )
        SELECT
            a.user_id,
            a.date,
            a.distance,
            a.elevation,
            m.efficiency_avg,
            m.hr_drift_avg,
            m.aerobic_decoupling_avg,
            m.avg_hr_percent_avg
        FROM activity_agg a
        LEFT JOIN metrics_agg m
            ON a.user_id = m.user_id AND a.date = m.date

        ON CONFLICT (user_id, date)
        DO UPDATE SET
            distance = EXCLUDED.distance,
            elevation = EXCLUDED.elevation,
            efficiency_avg = EXCLUDED.efficiency_avg,
            hr_drift_avg = EXCLUDED.hr_drift_avg,
            aerobic_decoupling_avg = EXCLUDED.aerobic_decoupling_avg,
            avg_hr_percent_avg = EXCLUDED.avg_hr_percent_avg;
    """)

    with engine.begin() as conn:
        conn.execute(query, {"user_id": user_id})