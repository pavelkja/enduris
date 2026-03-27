def generate_efficiency_insight(trend, confidence, variability):
        # edge cases (důležité!)
        if trend in ["not_enough_data", "insufficient_data"]:
            return {
                "headline": "Not enough data to evaluate performance",
                "subtext": None
            }

        # headline
        if trend == "improving":
            if confidence == "high":
                headline = "Efficiency is improving with high confidence"
            else:
                headline = "Efficiency is improving"

        elif trend == "declining":
            if confidence == "high":
                headline = "Efficiency is declining with high confidence"
            else:
                headline = "Efficiency is declining"

        else:
            headline = "Efficiency is stable"

        # variability
        if variability == "volatile":
            subtext = "Performance is inconsistent between activities"
        elif variability == "very_stable":
            subtext = "Performance is very consistent"
        else:
            subtext = None

        return {
            "headline": headline,
            "subtext": subtext
        }