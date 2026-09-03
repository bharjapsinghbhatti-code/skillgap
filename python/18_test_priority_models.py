import pandas as pd


# Load our current skill data
data = pd.read_csv(
    "data/processed/skill_priority_scores.csv"
)


# --------------------------------------------------
# Function for Min-Max normalization
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
# Normalize the three signals
# --------------------------------------------------

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
# Define our three models
# --------------------------------------------------

models = {

    "Entry Focused": {
        "entry": 0.60,
        "market": 0.20,
        "growth": 0.20
    },

    "Balanced": {
        "entry": 0.40,
        "market": 0.30,
        "growth": 0.30
    },

    "Career Growth": {
        "entry": 0.30,
        "market": 0.30,
        "growth": 0.40
    }
}


# --------------------------------------------------
# Calculate each model
# --------------------------------------------------

results = []

for model_name, weights in models.items():

    score = (
        data["entry_score"] * weights["entry"]
        +
        data["market_score"] * weights["market"]
        +
        data["growth_score_normalized"] * weights["growth"]
    )

    score = score * 100

    temp = data[
        [
            "canonical_skill"
        ]
    ].copy()

    temp["model"] = model_name
    temp["priority_score"] = score

    temp = temp.sort_values(
        "priority_score",
        ascending=False
    )

    temp["rank"] = range(
        1,
        len(temp) + 1
    )

    results.append(temp)


# --------------------------------------------------
# Combine results
# --------------------------------------------------

results = pd.concat(
    results,
    ignore_index=True
)


# --------------------------------------------------
# Save
# --------------------------------------------------

results.to_csv(
    "data/processed/priority_model_comparison.csv",
    index=False
)


# --------------------------------------------------
# Display top 10 for each model
# --------------------------------------------------

for model_name in models:

    print("\n===================================")
    print(model_name.upper())
    print("===================================")

    model_results = results[
        results["model"] == model_name
    ]

    print(
        model_results
        .head(10)
        .to_string(index=False)
    )


print("\nSaved to:")
print(
    "data/processed/priority_model_comparison.csv"
)