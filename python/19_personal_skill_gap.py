import pandas as pd


# --------------------------------------------------
# 1. Load SkillGap priority scores
# --------------------------------------------------

priority = pd.read_csv(
    "data/processed/skill_priority_scores.csv"
)


# --------------------------------------------------
# 2. Load user's current skills
# --------------------------------------------------

profile = pd.read_csv(
    "data/processed/my_skill_profile.csv"
)


# --------------------------------------------------
# 3. Merge profile with market intelligence
# --------------------------------------------------

data = priority.merge(
    profile,
    left_on="canonical_skill",
    right_on="skill",
    how="left"
)


# --------------------------------------------------
# 4. Missing skills are treated as level 0
# --------------------------------------------------

data["level"] = data["level"].fillna(0)


# --------------------------------------------------
# 5. Calculate skill gap
# --------------------------------------------------

data["skill_gap"] = (
    3 - data["level"]
)


# --------------------------------------------------
# 6. Calculate personalized priority
# --------------------------------------------------

data["personalized_priority"] = (
    data["priority_score"]
    * (data["skill_gap"] / 3)
)


# --------------------------------------------------
# 7. Sort recommendations
# --------------------------------------------------

recommendations = data.sort_values(
    "personalized_priority",
    ascending=False
)


# --------------------------------------------------
# 8. Save
# --------------------------------------------------

recommendations.to_csv(
    "data/processed/personal_skill_gap.csv",
    index=False
)


# --------------------------------------------------
# 9. Display
# --------------------------------------------------

print("===== PERSONAL SKILL GAP =====")

print(
    recommendations[
        [
            "canonical_skill",
            "level",
            "skill_gap",
            "priority_score",
            "personalized_priority"
        ]
    ].to_string(index=False)
)


print("\n===== TOP 5 RECOMMENDATIONS =====")

print(
    recommendations[
        [
            "canonical_skill",
            "personalized_priority"
        ]
    ]
    .head(5)
    .to_string(index=False)
)


print("\nSaved to:")
print(
    "data/processed/personal_skill_gap.csv"
)