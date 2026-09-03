import pandas as pd


# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

growth = pd.read_csv(
    "data/processed/skill_growth_scores.csv"
)

market = pd.read_csv(
    "data/processed/canonical_skill_demand_v2.csv"
)


# --------------------------------------------------
# 2. Keep required market information
# --------------------------------------------------

market = market[
    [
        "canonical_skill",
        "job_count",
        "demand_percentage",
        "skill_type"
    ]
]


# --------------------------------------------------
# 3. Merge datasets
# --------------------------------------------------

data = growth.merge(
    market,
    on="canonical_skill",
    how="left"
)


# --------------------------------------------------
# 4. Create Entry Demand
# --------------------------------------------------

data["entry_demand"] = data["Entry"]


# --------------------------------------------------
# 5. Normalize signals
# --------------------------------------------------

def min_max(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return 0.5

    return (
        (series - minimum)
        / (maximum - minimum)
    )


data["entry_score"] = min_max(
    data["entry_demand"]
)

data["market_score"] = min_max(
    data["demand_percentage"]
)

data["growth_score_normalized"] = min_max(
    data["growth_score"]
)


# --------------------------------------------------
# 6. Calculate Skill Priority Score
# --------------------------------------------------

data["priority_score"] = (
    data["entry_score"] * 0.40
    +
    data["market_score"] * 0.30
    +
    data["growth_score_normalized"] * 0.30
)


# Convert to 0–100
data["priority_score"] = (
    data["priority_score"] * 100
)


# --------------------------------------------------
# 7. Rank skills
# --------------------------------------------------

data = data.sort_values(
    "priority_score",
    ascending=False
)


data["priority_rank"] = range(
    1,
    len(data) + 1
)


# --------------------------------------------------
# 8. Save
# --------------------------------------------------

data.to_csv(
    "data/processed/skill_priority_scores.csv",
    index=False
)


# --------------------------------------------------
# 9. Display
# --------------------------------------------------

print("===== SKILL PRIORITY =====")

print(
    data[
        [
            "priority_rank",
            "canonical_skill",
            "skill_type",
            "entry_demand",
            "demand_percentage",
            "growth_score",
            "priority_score"
        ]
    ].to_string(index=False)
)


print("\nSaved to:")
print(
    "data/processed/skill_priority_scores.csv"
)