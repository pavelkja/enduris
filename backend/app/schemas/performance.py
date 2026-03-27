from pydantic import BaseModel
from typing import Optional

class PerformanceInsight(BaseModel):
    headline: str
    subtext: str


class PerformanceDebug(BaseModel):
    current: float
    peak: float
    recent: float
    baseline: float


class PerformanceSummary(BaseModel):
    sport_type: str
    current_vs_peak: float
    current_vs_recent: float
    consistency_score: float
    state: str
    insight: PerformanceInsight
    debug: PerformanceDebug

class PerformanceSummary(BaseModel):
    sport_type: str
    current_vs_peak: float
    current_vs_recent: float
    consistency_score: float
    state: str
    insight: PerformanceInsight
    coach_message: Optional[str] = None
    debug: PerformanceDebug