import pandas as pd

from engine.role_profiles import get_role_profile


class SkillGapEngine:

    def __init__(self):

        self.data = pd.read_csv(
            "data/processed/skill_progression_matrix.csv"
        )

        self.market = pd.read_csv(
            "data/processed/canonical_skill_demand_v2.csv"
        )

        self.data = self.data.merge(
            self.market[
                [
                    "canonical_skill",
                    "demand_percentage",
                    "skill_type"
                ]
            ],
            on="canonical_skill",
            how="left"
        )

    def get_skills(self):

        return sorted(
            self.data["canonical_skill"]
            .dropna()
            .unique()
            .tolist()
        )

    def recommend(
        self,
        current_skills,
        current_level="Entry",
        target_level="Senior",
        target_role="Data Analyst"
    ):

        result = self.data.copy()

        stages = [
            "Entry",
            "Junior",
            "Mid",
            "Senior"
        ]

        if current_level not in stages:
            raise ValueError(
                f"Invalid current level: {current_level}"
            )

        if target_level not in stages:
            raise ValueError(
                f"Invalid target level: {target_level}"
            )

        if stages.index(target_level) <= stages.index(current_level):
            raise ValueError(
                "Target level must be higher than current level."
            )

        # -------------------------------------------------
        # ROLE PROFILE
        # -------------------------------------------------

        role_profile = get_role_profile(target_role)

        result["role_relevance"] = (
            result["canonical_skill"]
            .map(role_profile)
            .fillna(0.30)
        )

        # -------------------------------------------------
        # CURRENT SKILLS
        # -------------------------------------------------

        normalized_skills = {}

        for skill, level in current_skills.items():

            level = int(level)

            if level < 0 or level > 3:
                raise ValueError(
                    f"Skill level for {skill} must be between 0 and 3."
                )

            normalized_skills[
                skill.lower().strip()
            ] = level

        result["current_skill_level"] = (
            result["canonical_skill"]
            .str.lower()
            .map(normalized_skills)
            .fillna(0)
            .astype(int)
        )

        # -------------------------------------------------
        # SKILL GAP
        # -------------------------------------------------

        result["personal_gap"] = (
            3 - result["current_skill_level"]
        )

        result["skill_gap"] = (
            result["personal_gap"] / 3 * 100
        )

        # -------------------------------------------------
        # CAREER GROWTH
        # -------------------------------------------------

        result["career_growth"] = (
            result[target_level]
            - result[current_level]
        )

        result = result[
            (result["personal_gap"] > 0)
            &
            (result["career_growth"] > 0)
        ].copy()

        # -------------------------------------------------
        # NORMALIZATION
        # -------------------------------------------------

        def min_max(series):

            minimum = series.min()
            maximum = series.max()

            if maximum == minimum:
                return pd.Series(
                    0.5,
                    index=series.index
                )

            return (
                (series - minimum)
                /
                (maximum - minimum)
            )

        result["market_score"] = min_max(
            result["demand_percentage"]
        )

        result["growth_score"] = min_max(
            result["career_growth"]
        )

        result["gap_score"] = (
            result["personal_gap"] / 3
        )

        # -------------------------------------------------
        # ROLE-AWARE PRIORITY SCORE
        #
        # Skill Gap       = 30%
        # Market Demand   = 20%
        # Career Growth   = 20%
        # Role Relevance  = 30%
        # -------------------------------------------------

        result["priority_score"] = (

            result["gap_score"] * 0.30

            +

            result["market_score"] * 0.20

            +

            result["growth_score"] * 0.20

            +

            result["role_relevance"] * 0.30

        ) * 100

        # -------------------------------------------------
        # PRIORITY LABEL
        # -------------------------------------------------

        def priority_label(score):

            if score >= 75:
                return "Critical"

            if score >= 50:
                return "High"

            if score >= 25:
                return "Medium"

            return "Low"

        result["priority"] = (
            result["priority_score"]
            .apply(priority_label)
        )

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        def category(row):

            target_demand = row[target_level]

            if target_demand >= 20:
                return "Core"

            if target_demand >= 10:
                return "Growth"

            return "Specialized"

        result["recommendation_type"] = (
            result.apply(category, axis=1)
        )

        # -------------------------------------------------
        # RECOMMENDATION REASON
        # -------------------------------------------------

        def recommendation_reason(row):

            reasons = []

            if row["skill_gap"] >= 66:
                reasons.append(
                    "large skill gap"
                )

            elif row["skill_gap"] >= 33:
                reasons.append(
                    "moderate skill gap"
                )

            if row["demand_percentage"] >= 20:
                reasons.append(
                    "strong market demand"
                )

            elif row["demand_percentage"] >= 10:
                reasons.append(
                    "good market demand"
                )

            if row["career_growth"] >= 20:
                reasons.append(
                    "high career progression value"
                )

            elif row["career_growth"] >= 10:
                reasons.append(
                    "useful career progression"
                )

            if row["role_relevance"] >= 0.80:
                reasons.append(
                    "high relevance to target role"
                )

            elif row["role_relevance"] >= 0.60:
                reasons.append(
                    "relevant to target role"
                )

            if not reasons:
                return (
                    "Relevant for your target career level."
                )

            return (
                "Recommended because of "
                + ", ".join(reasons)
                + "."
            )

        result["reason"] = (
            result.apply(
                recommendation_reason,
                axis=1
            )
        )

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        result = result.sort_values(
            "priority_score",
            ascending=False
        ).reset_index(drop=True)

        # -------------------------------------------------
        # ROUND VALUES
        # -------------------------------------------------

        result["priority_score"] = (
            result["priority_score"].round(2)
        )

        result["skill_gap"] = (
            result["skill_gap"].round(2)
        )

        result["demand_percentage"] = (
            result["demand_percentage"].round(2)
        )

        result["career_growth"] = (
            result["career_growth"].round(2)
        )

        # -------------------------------------------------
        # RETURN
        # -------------------------------------------------

        return {
            "core": result[
                result["recommendation_type"] == "Core"
            ].head(5),

            "growth": result[
                result["recommendation_type"] == "Growth"
            ].head(5),

            "specialized": result[
                result["recommendation_type"] == "Specialized"
            ].head(5),

            "all": result
        }