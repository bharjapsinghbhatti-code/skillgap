import pandas as pd


# Load role-skill data
data = pd.read_csv(
    "data/processed/role_skill_demand.csv"
)


# --------------------------------------------------
# Total jobs per role
# --------------------------------------------------

role_totals = (
    data[
        [
            "role_family",
            "total_jobs"
        ]
    ]
    .drop_duplicates()
)


# --------------------------------------------------
# Pivot demand
# --------------------------------------------------

pivot = data.pivot_table(
    index="canonical_skill",
    columns="role_family",
    values="demand_percentage",
    aggfunc="first"
).fillna(0)


# --------------------------------------------------
# Pivot job counts
# --------------------------------------------------

counts = data.pivot_table(
    index="canonical_skill",
    columns="role_family",
    values="job_count",
    aggfunc="first"
).fillna(0)


# --------------------------------------------------
# Calculate difference
# --------------------------------------------------

pivot["difference"] = (
    pivot["Data Analyst"]
    - pivot["Business Analyst"]
)


# --------------------------------------------------
# Add sample sizes
# --------------------------------------------------

data_analyst_total = (
    role_totals.loc[
        role_totals["role_family"] == "Data Analyst",
        "total_jobs"
    ]
    .iloc[0]
)

business_analyst_total = (
    role_totals.loc[
        role_totals["role_family"] == "Business Analyst",
        "total_jobs"
    ]
    .iloc[0]
)


# --------------------------------------------------
# Evidence classification
# --------------------------------------------------

def evidence_strength(row):

    max_count = max(
        row["Data Analyst"],
        row["Business Analyst"]
    )

    min_count = min(
        row["Data Analyst"],
        row["Business Analyst"]
    )

    difference = abs(
        row["difference"]
    )

    # Both roles have at least 20 postings
    if (
        min_count >= 20
        and difference >= 5
    ):
        return "Strong"

    elif (
        min_count >= 10
        and difference >= 3
    ):
        return "Moderate"

    else:
        return "Weak"


evidence = pivot.copy()

evidence["Data Analyst"] = (
    counts["Data Analyst"]
)

evidence["Business Analyst"] = (
    counts["Business Analyst"]
)

evidence["percentage_difference"] = (
    pivot["difference"]
)

evidence["evidence_strength"] = (
    evidence.apply(
        evidence_strength,
        axis=1
    )
)


# --------------------------------------------------
# Save
# --------------------------------------------------

evidence.to_csv(
    "data/processed/role_skill_evidence.csv"
)


# --------------------------------------------------
# Display
# --------------------------------------------------

print("===== ROLE DIFFERENTIATION EVIDENCE =====")

print(
    evidence[
        [
            "Data Analyst",
            "Business Analyst",
            "percentage_difference",
            "evidence_strength"
        ]
    ]
    .sort_values(
        "percentage_difference",
        key=abs,
        ascending=False
    )
    .head(20)
    .to_string()
)


print("\nRole sample sizes:")

print(
    f"Data Analyst: {data_analyst_total}"
)

print(
    f"Business Analyst: {business_analyst_total}"
)


print("\nSaved to:")
print(
    "data/processed/role_skill_evidence.csv"
)