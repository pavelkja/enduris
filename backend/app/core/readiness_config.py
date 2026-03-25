from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessConfig:
    EFFICIENCY_THRESHOLD: float = 0.02
    DRIFT_THRESHOLD: float = 0.05
    MIN_DATA_POINTS: int = 5
    HIGH_CONFIDENCE_THRESHOLD: int = 10
    STALE_DAYS: int = 10

    # Noise protection controls
    ROLLING_SHORT_WINDOW: int = 5
    ROLLING_LONG_WINDOW: int = 10
    ROBUST_AVERAGE_METHOD: str = "trimmed_mean"  # options: mean, median, trimmed_mean
    TRIM_RATIO: float = 0.1
