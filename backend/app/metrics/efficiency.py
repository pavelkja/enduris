def compute(activity, streams):
    if activity.avg_hr is None:
        return None

    if activity.avg_speed is None:
        return None

    efficiency = activity.avg_speed / activity.avg_hr

    return {
        "metric_name": "efficiency",
        "value": efficiency
    }