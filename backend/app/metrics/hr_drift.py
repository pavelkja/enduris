import json


def compute(activity, streams):

    if not streams:
        return None

    hr_stream = streams.get("heartrate")
    time_stream = streams.get("time")

    if not hr_stream or not time_stream:
        return None

    hr_raw = hr_stream.get("data")
    time_raw = time_stream.get("data")

    if not hr_raw or not time_raw:
        return None

    # 🔥 FIX: parse JSON string → list
    try:
        hr = json.loads(hr_raw) if isinstance(hr_raw, str) else hr_raw
        time = json.loads(time_raw) if isinstance(time_raw, str) else time_raw
    except Exception:
        return None

    # 🔹 minimální délka
    if len(hr) < 60:
        return None

    # 🔹 odstranění nesmyslů
    hr = [x for x in hr if x is not None and x > 0]

    if len(hr) < 60:
        return None

    n = len(hr)
    half = n // 2

    first_half = hr[:half]
    second_half = hr[half:]

    if not first_half or not second_half:
        return None

    hr_first = sum(first_half) / len(first_half)
    hr_second = sum(second_half) / len(second_half)

    if hr_first == 0:
        return None

    drift = (hr_second - hr_first) / hr_first

    return {
        "metric_name": "hr_drift",
        "value": drift
    }