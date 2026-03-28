from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity import Activity


CYCLING_OVERALL_SPORT_TYPES = [
    "Ride",
    "GravelRide",
    "MountainBikeRide",
    "VirtualRide",
]


def _normalize_sport_filter(sport: str) -> tuple[str, list[str]]:
    sport_map = {
        "ride": ["Ride"],
        "run": ["Run"],
        "cycling_overall": CYCLING_OVERALL_SPORT_TYPES,
    }

    normalized = sport.lower().strip()
    sport_types = sport_map.get(normalized)

    if not sport_types:
        raise ValueError(
            "Unsupported sport filter. Use one of: ride, run, cycling_overall"
        )

    return normalized, sport_types


def _empty_metrics() -> dict[str, float | int]:
    return {
        "distance": 0.0,
        "rides": 0,
        "elevation": 0.0,
        "time": 0,
        "avg_hr": 0.0,
    }


def _aggregate_metrics(
    db: Session,
    user_id: str,
    sport_types: list[str],
    start: datetime,
    end: datetime,
) -> dict[str, float | int]:

    totals = (
        db.query(
            func.sum(Activity.distance).label("distance"),
            func.count(Activity.id).label("rides"),
            func.sum(Activity.elevation_gain).label("elevation"),
            func.sum(Activity.moving_time).label("time"),
            # weighted avg HR
            (
                func.sum(Activity.avg_hr * Activity.moving_time)
                / func.nullif(func.sum(Activity.moving_time), 0)
            ).label("avg_hr"),
        )
        .filter(
            Activity.user_id == user_id,
            Activity.sport_type.in_(sport_types),
            Activity.start_date >= start,
            Activity.start_date < end,
            Activity.avg_hr.isnot(None),  # IMPORTANT FIX
        )
        .one()
    )

    if not totals.rides:
        return _empty_metrics()

    return {
        "distance": round(float(totals.distance or 0.0) / 1000.0, 2),
        "rides": int(totals.rides or 0),
        "elevation": round(float(totals.elevation or 0.0), 2),
        "time": int(totals.time or 0),
        "avg_hr": round(float(totals.avg_hr or 0.0), 2),
    }


def get_dashboard_ytd(db: Session, user_id: str, sport: str) -> list[dict[str, Any]]:
    _, sport_types = _normalize_sport_filter(sport)

    now = datetime.now(timezone.utc)
    current_year = now.year

    response: list[dict[str, Any]] = []

    for year in [current_year, current_year - 1, current_year - 2]:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)

        if year == current_year:
            end = now
        else:
            end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)

        response.append(
            {
                "year": year,
                "metrics": _aggregate_metrics(db, user_id, sport_types, start, end),
            }
        )

    return response


def _first_day_of_month(ts: datetime) -> datetime:
    return datetime(ts.year, ts.month, 1, tzinfo=timezone.utc)


def _shift_month(ts: datetime, months: int) -> datetime:
    year = ts.year
    month = ts.month + months

    while month <= 0:
        month += 12
        year -= 1

    while month > 12:
        month -= 12
        year += 1

    return datetime(year, month, 1, tzinfo=timezone.utc)


def get_dashboard_months(db: Session, user_id: str, sport: str) -> list[dict[str, Any]]:
    _, sport_types = _normalize_sport_filter(sport)

    now = datetime.now(timezone.utc)
    current_month = _first_day_of_month(now)

    monthly_windows = [
        ("current_month", current_month),
        ("same_month_last_year", _shift_month(current_month, -12)),
        ("same_month_two_years", _shift_month(current_month, -24)),
        ("previous_month", _shift_month(current_month, -1)),
        ("previous_month_last_year", _shift_month(current_month, -13)),
    ]

    response: list[dict[str, Any]] = []

    for label, month_start in monthly_windows:
        month_end = _shift_month(month_start, 1)

        response.append(
            {
                "label": label,
                "month": month_start.strftime("%Y-%m"),
                "metrics": _aggregate_metrics(
                    db, user_id, sport_types, month_start, month_end
                ),
            }
        )

    return response
