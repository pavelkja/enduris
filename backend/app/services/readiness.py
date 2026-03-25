from __future__ import annotations

from datetime import datetime, timezone
from statistics import median
from typing import Dict, List, Optional

from app.core.readiness_config import ReadinessConfig


class ReadinessService:
    def __init__(self, metrics_repository, config: Optional[ReadinessConfig] = None):
        self.metrics_repository = metrics_repository
        self.config = config or ReadinessConfig()

    def get_readiness(self, user_id: str, sport_type: str) -> Dict:
        activities = self.metrics_repository.get_last_activities_with_metrics(
            user_id=user_id,
            sport_type=sport_type,
            limit=self.config.ROLLING_LONG_WINDOW,
        )

        latest_activity_date = self.metrics_repository.get_latest_activity_date(
            user_id=user_id,
            sport_type=sport_type,
        )

        if not activities:
            return self._build_response(
                status="no_data",
                confidence="low",
                recency_status=self._compute_recency_status(latest_activity_date),
                model_type="primary",
                reason="Insufficient activity data to evaluate readiness",
                efficiency_delta=0.0,
                hr_drift=None,
                data_points=0,
                hr_drift_points=0,
            )

        activities = sorted(
            activities,
            key=lambda activity: activity.get("start_date") or datetime.min,
            reverse=True,
        )

        efficiency_values = [
            value
            for value in (activity.get("efficiency") for activity in activities)
            if self._is_valid_efficiency(value)
        ]
        hr_drift_values = [
            value
            for value in (activity.get("hr_drift") for activity in activities)
            if self._is_valid_hr_drift(value)
        ]

        data_points = len(efficiency_values)
        hr_drift_points = len(hr_drift_values)

        efficiency_last_5_avg = self._robust_average(
            efficiency_values[: self.config.ROLLING_SHORT_WINDOW]
        )
        efficiency_last_10_avg = self._robust_average(
            efficiency_values[: self.config.ROLLING_LONG_WINDOW]
        )

        hr_drift_avg = None
        if hr_drift_points >= self.config.MIN_DATA_POINTS:
            hr_drift_avg = self._robust_average(
                hr_drift_values[: self.config.ROLLING_LONG_WINDOW]
            )

        if not efficiency_values:
            return self._build_response(
                status="no_data",
                confidence=self._compute_confidence(data_points),
                recency_status=self._compute_recency_status(latest_activity_date),
                model_type="primary",
                reason="Missing efficiency data",
                efficiency_delta=0.0,
                hr_drift=None,
                data_points=data_points,
                hr_drift_points=hr_drift_points,
            )

        return self.evaluate_readiness(
            efficiency_last_5_avg=efficiency_last_5_avg,
            efficiency_last_10_avg=efficiency_last_10_avg,
            hr_drift_avg=hr_drift_avg,
            data_points=data_points,
            hr_drift_points=hr_drift_points,
            latest_activity_date=latest_activity_date,
        )

    def evaluate_readiness(
        self,
        efficiency_last_5_avg: Optional[float],
        efficiency_last_10_avg: Optional[float],
        hr_drift_avg: Optional[float],
        data_points: Optional[int],
        hr_drift_points: Optional[int],
        latest_activity_date: Optional[datetime],
    ) -> Dict:
        safe_data_points = max(0, int(data_points or 0))
        safe_hr_drift_points = max(0, int(hr_drift_points or 0))
        confidence = self._compute_confidence(safe_data_points)
        recency_status = self._compute_recency_status(latest_activity_date)

        if efficiency_last_5_avg is None or efficiency_last_10_avg is None:
            return self._build_response(
                status="no_data",
                confidence=confidence,
                recency_status=recency_status,
                model_type="primary",
                reason="Insufficient efficiency data",
                efficiency_delta=0.0,
                hr_drift=hr_drift_avg,
                data_points=safe_data_points,
                hr_drift_points=safe_hr_drift_points,
            )

        efficiency_delta = self._compute_relative_efficiency_delta(
            efficiency_last_5_avg,
            efficiency_last_10_avg,
        )

        is_enhanced_mode = (
            safe_hr_drift_points >= self.config.MIN_DATA_POINTS and hr_drift_avg is not None
        )
        model_type = "enhanced" if is_enhanced_mode else "primary"

        if is_enhanced_mode:
            # Narrow Optional[float] for static analyzers (pyright/mypy).
            assert hr_drift_avg is not None
            if (
                efficiency_delta > self.config.EFFICIENCY_THRESHOLD
                and hr_drift_avg <= self.config.DRIFT_THRESHOLD
            ):
                status = "good_day"
                reason = "Efficiency improving and HR drift stable"
            elif (
                efficiency_delta < -self.config.EFFICIENCY_THRESHOLD
                and hr_drift_avg > self.config.DRIFT_THRESHOLD
            ):
                status = "fatigue"
                reason = "Efficiency declining and HR drift increasing"
            else:
                status = "caution"
                reason = "Mixed signals between efficiency and HR drift"
        else:
            if efficiency_delta > self.config.EFFICIENCY_THRESHOLD:
                status = "good_day"
                reason = "Efficiency improving"
            elif efficiency_delta < -self.config.EFFICIENCY_THRESHOLD:
                status = "caution"
                reason = "Efficiency declining"
            else:
                status = "caution"
                reason = "Efficiency stable"

        return self._build_response(
            status=status,
            confidence=confidence,
            recency_status=recency_status,
            model_type=model_type,
            reason=reason,
            efficiency_delta=efficiency_delta,
            hr_drift=hr_drift_avg if is_enhanced_mode else None,
            data_points=safe_data_points,
            hr_drift_points=safe_hr_drift_points,
        )

    def _compute_confidence(self, data_points: int) -> str:
        if data_points < self.config.MIN_DATA_POINTS:
            return "low"
        if data_points >= self.config.HIGH_CONFIDENCE_THRESHOLD:
            return "high"
        return "medium"

    def _compute_recency_status(self, latest_activity_date: Optional[datetime]) -> str:
        if latest_activity_date is None:
            return "stale"

        now = datetime.now(timezone.utc)
        if latest_activity_date.tzinfo is None:
            latest_activity_date = latest_activity_date.replace(tzinfo=timezone.utc)
        else:
            latest_activity_date = latest_activity_date.astimezone(timezone.utc)

        age_days = (now - latest_activity_date).days
        return "stale" if age_days > self.config.STALE_DAYS else "fresh"

    def _robust_average(self, values: List[float]) -> Optional[float]:
        if not values:
            return None

        method = self.config.ROBUST_AVERAGE_METHOD.lower()
        sorted_values = sorted(values)

        if method == "median":
            return float(median(sorted_values))

        if method == "trimmed_mean":
            trim_count = int(len(sorted_values) * self.config.TRIM_RATIO)
            if trim_count > 0 and len(sorted_values) > (2 * trim_count):
                sorted_values = sorted_values[trim_count:-trim_count]

        return float(sum(sorted_values) / len(sorted_values))

    def _compute_relative_efficiency_delta(self, last_5_avg: float, last_10_avg: float) -> float:
        if last_10_avg == 0:
            return 0.0
        return (last_5_avg - last_10_avg) / last_10_avg

    def _is_valid_efficiency(self, value: Optional[float]) -> bool:
        return value is not None and 0 < value < 0.2

    def _is_valid_hr_drift(self, value: Optional[float]) -> bool:
        return value is not None and 0 <= value < 0.2

    def _build_response(
        self,
        status: str,
        confidence: str,
        recency_status: str,
        model_type: str,
        reason: str,
        efficiency_delta: float,
        hr_drift: Optional[float],
        data_points: int,
        hr_drift_points: int,
    ) -> Dict:
        return {
            "status": status,
            "confidence": confidence,
            "recency_status": recency_status,
            "model_type": model_type,
            "reason": reason,
            "metrics": {
                "efficiency_delta": round(float(efficiency_delta), 6),
                "hr_drift": None if hr_drift is None else round(float(hr_drift), 6),
            },
            "data_points": data_points,
            "hr_drift_points": hr_drift_points,
        }
