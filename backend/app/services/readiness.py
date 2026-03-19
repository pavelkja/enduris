from typing import List, Dict, Optional
from datetime import datetime


class ReadinessService:
            def __init__(self, metrics_repository):
                self.metrics_repository = metrics_repository

            def get_readiness(self, user_id: str, sport_type: str, limit: int = 7) -> Dict:

                activities = self.metrics_repository.get_last_activities_with_metrics(
                    user_id=user_id,
                    sport_type=sport_type,
                    limit=limit
                )

                print("==== READINESS DEBUG ====")
                print("activities count:", len(activities))
                print("sample activities:", activities[:3])

                if not activities:
                    print("❌ No activities returned from repository")
                    return self._not_enough_data()

                # 👉 NEW: latest activity + recency
                latest_date = self.metrics_repository.get_latest_activity_date(
                    user_id=user_id,
                    sport_type=sport_type
                )

                recency_status = self._compute_recency_status(latest_date)

                efficiencies = [
                    a["efficiency"] for a in activities
                    if a.get("efficiency") is not None
                ]

                hr_drifts = [
                    a["hr_drift"] for a in activities
                    if a.get("hr_drift") is not None
                ]

                print("efficiencies count:", len(efficiencies))
                print("hr_drifts count:", len(hr_drifts))

                # -------------------------
                # TRENDY (fallback-safe)
                # -------------------------

                efficiency_trend: Optional[str] = (
                    self._compute_trend(efficiencies) if len(efficiencies) >= 3 else None
                )

                drift_trend: Optional[str] = (
                    self._compute_trend(hr_drifts) if len(hr_drifts) >= 3 else None
                )

                print("eff trend:", efficiency_trend)
                print("drift trend:", drift_trend)

                if efficiency_trend is None and drift_trend is None:
                    print("❌ No usable trends")
                    return self._not_enough_data()

                # -------------------------
                # SCORING
                # -------------------------

                score = 0

                if efficiency_trend == "up":
                    score += 1
                elif efficiency_trend == "down":
                    score -= 1

                if drift_trend == "up":
                    score -= 1
                elif drift_trend == "down":
                    score += 1

                print("score:", score)

                # -------------------------
                # CONFIDENCE (UPDATED)
                # -------------------------

                if hr_drifts:
                    data_points = min(len(efficiencies), len(hr_drifts))
                else:
                    data_points = len(efficiencies)

                confidence = self._compute_confidence(data_points, recency_status)

                print("confidence:", confidence)
                print("recency_status:", recency_status)

                # -------------------------
                # FINAL OUTPUT
                # -------------------------

                result = self._interpret(score, efficiency_trend, drift_trend, confidence)

                # 👉 NEW: doplnění meta info
                result["recency_status"] = recency_status
                result["latest_activity_date"] = (
                    latest_date.isoformat() if latest_date else None
                )
                result["data_points"] = data_points

                return result

            # -------------------------

            def _compute_trend(self, values: List[float]) -> str:

                if len(values) < 6:
                    print("⚠️ Not enough values for full trend → fallback trend")

                    recent_avg = sum(values[:3]) / len(values[:3])
                    overall_avg = sum(values) / len(values)

                    diff = recent_avg - overall_avg
                else:
                    recent = values[:3]
                    previous = values[3:6]

                    recent_avg = sum(recent) / len(recent)
                    previous_avg = sum(previous) / len(previous)

                    diff = recent_avg - previous_avg

                threshold = 0.02

                print("trend calc diff:", diff)

                if diff > threshold:
                    return "up"
                elif diff < -threshold:
                    return "down"
                else:
                    return "stable"

            # -------------------------

            def _compute_recency_status(self, latest_date) -> str:
                if not latest_date:
                    return "no_data"

                delta = (datetime.utcnow() - latest_date).days

                if delta < 7:
                    return "fresh"
                elif delta <= 21:
                    return "moderate"
                return "stale"

            # -------------------------

            def _compute_confidence(self, data_points: int, recency_status: str) -> str:
                if data_points < 5:
                    return "low"

                if recency_status == "fresh":
                    return "high"
                elif recency_status == "moderate":
                    return "medium"

                return "low"

            # -------------------------

            def _interpret(
                self,
                score: int,
                efficiency_trend: Optional[str],
                drift_trend: Optional[str],
                confidence: str
            ) -> Dict:

                # 🔴 tired
                if score <= -1:
                    return {
                        "status": "tired",
                        "headline": "Dneska spíš klid",
                        "message": "Výkon klesá nebo se zhoršuje efektivita.",
                        "coach_message": "Dej si lehkou aktivitu nebo pauzu.",
                        "confidence": confidence
                    }

                # 🟢 good day
                if score >= 1:
                    return {
                        "status": "good_day",
                        "headline": "Dneska to půjde",
                        "message": "Tělo reaguje dobře a zvládá zátěž.",
                        "coach_message": "Klidně můžeš přidat.",
                        "confidence": confidence
                    }

                # 🟡 ready
                return {
                    "status": "ready",
                    "headline": "Jsi ready",
                    "message": "Bez výrazného trendu, ale stabilní stav.",
                    "coach_message": "Jdi podle pocitu.",
                    "confidence": confidence
                }

            # -------------------------

            def _not_enough_data(self) -> Dict:
                return {
                    "status": "no_data",
                    "headline": "Málo dat",
                    "message": "Potřebuju víc aktivit pro vyhodnocení.",
                    "coach_message": "Ještě chvíli jezdi 🙂",
                    "confidence": "low"
                }