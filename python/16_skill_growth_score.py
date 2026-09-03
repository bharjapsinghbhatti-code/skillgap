import pandas as pd


# Load progression matrix
matrix = pd.read_csv(
    "data/processed/skill_progression_matrix.csv"
)


# --------------------------------------------------
# Calculate growth from Entry → Senior
# --------------------------------------------------

matrix["growth_score"] = (
    matrix["Senior"]
    - matrix["Entry"]
)


# --------------------------------------------------
# Classify skill progression
# --------------------------------------------------

def classify_growth(score):

    if score >= 10:
        return "Strong Growth"

    elif score >= 3:
        return "Moderate Growth"

    elif score <= -10:
        return "Strong Decline"

    elif score <= -3:
        return "Moderate Decline"

    else:
        return "Stable"


matrix["progression_type"] = (
    matrix["growth_score"]
    .apply(classify_growth)
)


# --------------------------------------------------
# Sort by growth
# --------------------------------------------------

matrix = matrix.sort_values(
    "growth_score",
    ascending=False
)


# --------------------------------------------------
# Save
# --------------------------------------------------

matrix.to_csv(
    "data/processed/skill_growth_scores.csv",
    index=False
)


# --------------------------------------------------
# Display
# --------------------------------------------------

print("===== SKILL GROWTH SCORES =====")

print(
    matrix[
        [
            "canonical_skill",
            "Entry",
            "Senior",
            "growth_score",
            "progression_type"
        ]
    ].to_string(index=False)
)


print("\nSaved to:")
print(
    "data/processed/skill_growth_scores.csv"
)