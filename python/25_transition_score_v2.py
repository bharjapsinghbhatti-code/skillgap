import pandas as pd


# --------------------------------------------------
# 1. Load transition data
# --------------------------------------------------

data = pd.read_csv(
    "data/processed/career_transition_recommendations.csv"
)


# --------------------------------------------------
# 2. Min-Max normalization
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


# --------------------------------------------------
# 3. Market relevance
# --------------------------------------------------

# Senior-level demand tells us how widely
# the skill appears in senior Data Analyst jobs.

data["market_score"] = min_max(
    data["Senior"]
)


# --------------------------------------------------
# 4. Career growth
# --------------------------------------------------

data["growth_score"] = min_max(
    data["transition_growth"]
)


# --------------------------------------------------
# 5. Personal gap
# --------------------------------------------------

data["gap_score"] = (
    data["personal_gap"] / 3
)


# --------------------------------------------------
# 6. Calculate raw transition score
# --------------------------------------------------

data["transition_score"] = (
    data["market_score"] * 0.40
    +
    data["growth_score"] * 0.30
    +
    data["gap_score"] * 0.30
)


data["transition_score"] = (
    data["transition_score"] * 100
)


# --------------------------------------------------
# 7. Remove skills already mastered
# --------------------------------------------------

data = data[
    data["personal_gap"] > 0
]


# --------------------------------------------------
# 8. Remove skills with no positive growth
# --------------------------------------------------

data = data[
    data["transition_growth"] > 0
]


# --------------------------------------------------
# 9. Add market relevance categories
# --------------------------------------------------

def market_category(senior_demand):

    if senior_demand >= 20:
        return "Core"

    elif senior_demand >= 10:
        return "Growth"

    else:
        return "Specialized"


data["market_category"] = (
    data["Senior"]
    .apply(market_category)
)


# --------------------------------------------------
# 10. Sort AFTER all filtering
# --------------------------------------------------

data = data.sort_values(
    "transition_score",
    ascending=False
).reset_index(drop=True)


# --------------------------------------------------
# 11. Assign correct ranks
# --------------------------------------------------

data["rank"] = (
    data.index + 1
)


# --------------------------------------------------
# 12. Save
# --------------------------------------------------

data.to_csv(
    "data/processed/transition_scores_v3.csv",
    index=False
)


# --------------------------------------------------
# 13. Display
# --------------------------------------------------

print("===== CAREER TRANSITION SCORE V3 =====")

print(
    data[
        [
            "rank",
            "canonical_skill",
            "market_category",
            "Entry",
            "Senior",
            "personal_gap",
            "transition_growth",
            "transition_score"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


# --------------------------------------------------
# 14. Category summary
# --------------------------------------------------

print("\n===== RECOMMENDATION CATEGORIES =====")

print(
    data["market_category"]
    .value_counts()
)


print("\nSaved to:")
print(
    "data/processed/transition_scores_v3.csv"
)