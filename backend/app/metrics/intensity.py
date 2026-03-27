# app/metrics/intensity.py

def compute_avg_hr_percent(activity, user):
    """
    Computes average HR intensity relative to user's max HR.

    avg_hr_percent = avg_hr / max_hr
    """

    if activity.avg_hr is None:
        return None

    if user.max_hr is None:
        return None

    if user.max_hr == 0:
        return None

    avg_hr_percent = activity.avg_hr / user.max_hr

    return avg_hr_percent