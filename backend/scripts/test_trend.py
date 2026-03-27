from app.services.trends import get_efficiency_trend_with_insight

user_id = "b506b832-76f2-48f2-b1a1-e00ccef8b988"

sport_type = "Ride"

result = get_efficiency_trend_with_insight(user_id, sport_type)

print(result)