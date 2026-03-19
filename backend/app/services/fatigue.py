def detect_fatigue(metrics):

    valid = [
        m for m in metrics
        if m.efficiency is not None and m.hr_drift is not None
    ]

    count = len(valid)

    if count < 3:
        return {
            "fatigue_detected": False,
            "confidence": "low",
            "reason": "not_enough_data"
        }

    eff = [m.efficiency for m in valid]
    drift = [m.hr_drift for m in valid]

    # adaptive window
    window = min(5, count)
    baseline_window = min(10, count)

    eff_recent = sum(eff[-window:]) / window
    eff_baseline = sum(eff[-baseline_window:]) / baseline_window

    drift_recent = sum(drift[-window:]) / window
    drift_baseline = sum(drift[-baseline_window:]) / baseline_window

    # ochrana proti dělení nulou
    if eff_baseline == 0 or drift_baseline == 0:
        return {
            "fatigue_detected": False,
            "confidence": "low",
            "reason": "invalid_baseline"
        }

    eff_drop = (eff_recent - eff_baseline) / eff_baseline
    drift_increase = (drift_recent - drift_baseline) / drift_baseline

    fatigue = eff_drop < -0.05 and drift_increase > 0.05

    # confidence scoring
    if count >= 10:
        confidence = "high"
    elif count >= 5:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "fatigue_detected": fatigue,
        "confidence": confidence,
        "data_points": count,
        "eff_drop": eff_drop,
        "drift_increase": drift_increase,
    }