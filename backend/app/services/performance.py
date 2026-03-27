from fastapi import HTTPException
import statistics

from app.repositories.activities import get_activities_with_efficiency
from app.repositories.metrics_repository import MetricsRepository
from app.services.fatigue import detect_fatigue


def get_performance_summary(db, user_id: str, sport_type: str):

    # 🔹 MAIN DATA (zatím necháváme)
    result = get_activities_with_efficiency(db, user_id, sport_type)

    efficiencies = [row.efficiency for row in result if row.efficiency is not None]

    if len(efficiencies) < 10:
        raise HTTPException(status_code=400, detail="Not enough valid data")

    # 🔹 CURRENT (last 7)
    current = sum(efficiencies[-7:]) / min(7, len(efficiencies))

    # 🔹 RECENT (last 10)
    recent = sum(efficiencies[-10:]) / min(10, len(efficiencies))

    # 🔹 BASELINE (last 50)
    baseline = sum(efficiencies[-50:]) / min(50, len(efficiencies))

    # 🔹 PEAK (rolling avg 10)
    rolling_10 = [
        sum(efficiencies[i:i+10]) / 10
        for i in range(len(efficiencies) - 9)
    ]

    if not rolling_10:
        raise HTTPException(status_code=400, detail="Not enough data for rolling average")

    peak = max(rolling_10)

    # 🔹 COMPARISONS
    current_vs_peak = (current - peak) / peak * 100 if peak != 0 else 0
    current_vs_recent = (current - recent) / recent * 100 if recent != 0 else 0

    # 🔹 CONSISTENCY
    last_30 = efficiencies[-30:]
    std = statistics.stdev(last_30) if len(last_30) > 1 else 0
    consistency_score = max(0, 100 - (std * 10000))

    # 🔹 STATE LOGIC
    if current_vs_peak > -2:
        state = "near_peak"
    elif current_vs_peak > -6:
        state = "maintaining"
    elif current_vs_recent < -3:
        state = "declining"
    elif current_vs_recent > 3:
        state = "improving"
    else:
        state = "plateau"

    # 🔹 INSIGHT TEXT
    if state == "near_peak":
        headline = "You're near your peak"
        subtext = "Performance is at a very high level"

    elif state == "maintaining":
        headline = "You're maintaining fitness"
        subtext = "Slightly below peak, but stable"

    elif state == "declining":
        headline = "Performance is declining"
        subtext = "Recent sessions are weaker than usual"

    elif state == "improving":
        headline = "You're improving"
        subtext = "Recent sessions show positive trend"

    else:  # plateau
        if current_vs_peak < -7:
            headline = "You're below your peak"
            subtext = "Performance is stable, but noticeably lower than your best level"
        else:
            headline = "You're on a plateau"
            subtext = "No significant change in performance"

    # 🔥 FATIGUE DETECTION (UPDATED)
    repo = MetricsRepository(db)

    metrics = repo.get_last_activities_with_metrics(
        user_id=user_id,
        sport_type=sport_type,
        limit=20
    )

    fatigue = detect_fatigue(metrics)

    # 🔥 COACH MESSAGE
    if fatigue.get("fatigue_detected"):
        coach_message = "You look fatigued. Consider rest or easier sessions."

    elif state == "plateau" and current_vs_peak < -7:
        coach_message = "You've lost some peak fitness. Consider adding intensity or structured training."

    elif state == "declining":
        coach_message = "Recent performance is dropping. You may need recovery or reduced load."

    elif state == "improving":
        coach_message = "Training is working. Stay consistent."

    elif state == "near_peak":
        coach_message = "You're performing at a high level. Focus on maintaining consistency."

    else:
        coach_message = None

    return {
        "sport_type": sport_type,
        "current_vs_peak": round(current_vs_peak, 2),
        "current_vs_recent": round(current_vs_recent, 2),
        "consistency_score": round(consistency_score, 1),
        "state": state,
        "insight": {
            "headline": headline,
            "subtext": subtext
        },
        "fatigue": fatigue,
        "coach_message": coach_message,
        "debug": {
            "current": current,
            "peak": peak,
            "recent": recent,
            "baseline": baseline
        }
    }