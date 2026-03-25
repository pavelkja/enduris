import json
import math


MIN_DURATION_SECONDS = 20 * 60
MIN_SAMPLES = 60
MAX_HR_CV = 0.1
MAX_SPEED_CV = 0.2
CYCLING_SPORT_TYPES = {"Ride", "VirtualRide", "GravelRide", "MountainBikeRide"}


def _to_list(raw):
    if raw is None:
        return None
    if isinstance(raw, str):
        return json.loads(raw)
    return raw


def _mean(values):
    if not values:
        return None
    return sum(values) / len(values)


def _std(values, mean_value):
    if not values:
        return None
    variance = sum((x - mean_value) ** 2 for x in values) / len(values)
    return math.sqrt(variance)
    
    
def compute(activity, streams):

    if not streams:
        return None

    hr_stream = streams.get("heartrate")
    time_stream = streams.get("time")
    speed_stream = streams.get("speed")

    if not hr_stream or not time_stream:
        return None

    try:
        hr_raw = _to_list(hr_stream.get("data"))
        time_raw = _to_list(time_stream.get("data"))
        speed_raw = _to_list(speed_stream.get("data")) if speed_stream else None
    except Exception:
        return None

    if not isinstance(hr_raw, list) or not isinstance(time_raw, list):
            return None

    hr = [x for x in hr_raw if isinstance(x, (int, float)) and x > 0]
    time = [x for x in time_raw if isinstance(x, (int, float))]

    if len(hr) < MIN_SAMPLES or len(time) < 2:
        return None

    duration_seconds = time[-1] - time[0]
    if duration_seconds <= 0:
        duration_seconds = float(len(time))

        hr_mean = _mean(hr)
        if hr_mean is None or hr_mean <= 0:
            return None

        hr_std = _std(hr, hr_mean)
        hr_cv = hr_std / hr_mean

        sport_type = getattr(activity, "sport_type", None)
        is_cycling = sport_type in CYCLING_SPORT_TYPES

        speed_cv = 0.0
        if is_cycling:
            if not isinstance(speed_raw, list):
                print(
                    f"HR drift eligibility | activity={activity.id} duration={duration_seconds:.1f}s "
                    f"hr_cv={hr_cv:.4f} speed_cv=N/A eligible=False (missing cycling speed stream)"
                )
                return None

            speed = [x for x in speed_raw if isinstance(x, (int, float)) and x > 0]
            speed_mean = _mean(speed)
            if not speed or speed_mean is None or speed_mean <= 0:
                print(
                    f"HR drift eligibility | activity={activity.id} duration={duration_seconds:.1f}s "
                    f"hr_cv={hr_cv:.4f} speed_cv=N/A eligible=False (invalid cycling speed stream)"
                )
                return None

            speed_std = _std(speed, speed_mean)
            speed_cv = speed_std / speed_mean

        is_drift_eligible = (
            duration_seconds >= MIN_DURATION_SECONDS
            and hr_cv < MAX_HR_CV
            and (not is_cycling or speed_cv < MAX_SPEED_CV)
        )

        print(
            f"HR drift eligibility | activity={activity.id} duration={duration_seconds:.1f}s "
            f"hr_cv={hr_cv:.4f} speed_cv={speed_cv:.4f} eligible={is_drift_eligible}"
        )

        if not is_drift_eligible:
          return None

    n = len(hr)
    half = n // 2
    first_half = hr[:half]
    second_half = hr[half:]

    if not first_half or not second_half:
        return None

    hr_first = _mean(first_half)
    hr_second = _mean(second_half)

    if hr_first is None or hr_first == 0 or hr_second is None:
        return None

    drift = (hr_second - hr_first) / hr_first

    return {
        "metric_name": "hr_drift",
        "value": drift,
        "is_drift_eligible": is_drift_eligible,
        }
