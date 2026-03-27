from sqlalchemy import text


def get_activities_with_efficiency(db, user_id: str, sport_type: str):
    query = text("""
        SELECT 
            a.start_date,
            m.value as efficiency
        FROM activities a
        JOIN activity_metrics m 
            ON a.id = m.activity_id
        WHERE 
            a.user_id = :user_id
            AND a.sport_type = :sport_type
            AND m.metric_name = 'efficiency'
        ORDER BY a.start_date;
    """)

    result = db.execute(query, {
        "user_id": user_id,
        "sport_type": sport_type
    })

    return result.fetchall()