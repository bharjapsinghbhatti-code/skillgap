import pandas as pd


# --------------------------------------------------
# 1. Load progression data
# --------------------------------------------------

progression = pd.read_csv(
    "data/processed/skill_progression_matrix.csv"
)


# --------------------------------------------------
# 2. Load personal profile
# --------------------------------------------------

profile = pd.read_csv(
    "data/processed/my_skill_profile.csv"
)


# --------------------------------------------------
# 3. Merge profile
# --------------------------------------------------

data = progression.merge(
    profile,
    left_on="canonical_skill",
    right_on="skill",
    how="left"
)


# --------------------------------------------------
# 4. Missing skills = level 0
# --------------------------------------------------

data["level"] = data["level"].fillna(0)


# --------------------------------------------------
# 5. Calculate transition demand
# --------------------------------------------------

data["transition_growth"] = (
    data["Senior"]
    - data["Entry"]
)


# --------------------------------------------------
# 6. Calculate personal gap
# --------------------------------------------------

data["personal_gap"] = (
    3 - data["level"]
)


# --------------------------------------------------
# 7. Calculate transition priority
# --------------------------------------------------

data["transition_priority"] = (
    data["transition_growth"].clip(lower=0)
    *
    data["personal_gap"]
)


# --------------------------------------------------
# 8. Sort
# --------------------------------------------------

data = data.sort_values(
    "transition_priority",
    ascending=False
)


# --------------------------------------------------
# 9. Save
# --------------------------------------------------

data.to_csv(
    "data/processed/career_transition_recommendations.csv",
    index=False
)


# --------------------------------------------------
# 10. Display
# --------------------------------------------------

print("===== CAREER TRANSITION RECOMMENDATIONS =====")

print(
    data[
        [
            "canonical_skill",
            "Entry",
            "Senior",
            "level",
            "personal_gap",
            "transition_growth",
            "transition_priority"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\nSaved to:")
print(
    "data/processed/career_transition_recommendations.csv"
)