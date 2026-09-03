import pandas as pd


# --------------------------------------------------
# 1. Load role-skill data
# --------------------------------------------------

data = pd.read_csv(
    "data/processed/role_skill_demand.csv"
)


# --------------------------------------------------
# 2. Convert roles into columns
# --------------------------------------------------

pivot = data.pivot_table(
    index="canonical_skill",
    columns="role_family",
    values="demand_percentage",
    aggfunc="first"
).fillna(0)


# --------------------------------------------------
# 3. Calculate Data Analyst advantage
# --------------------------------------------------

pivot["data_analyst_advantage"] = (
    pivot["Data Analyst"]
    - pivot["Business Analyst"]
)


# --------------------------------------------------
# 4. Absolute difference
# --------------------------------------------------

pivot["absolute_difference"] = (
    pivot["data_analyst_advantage"]
    .abs()
)


# --------------------------------------------------
# 5. Sort by strongest differentiation
# --------------------------------------------------

pivot = pivot.sort_values(
    "absolute_difference",
    ascending=False
)


# --------------------------------------------------
# 6. Save
# --------------------------------------------------

pivot.to_csv(
    "data/processed/role_differentiation.csv"
)


# --------------------------------------------------
# 7. Display Data Analyst differentiators
# --------------------------------------------------

print("===== DATA ANALYST DIFFERENTIATORS =====")

print(
    pivot[
        pivot["data_analyst_advantage"] > 0
    ][
        [
            "Data Analyst",
            "Business Analyst",
            "data_analyst_advantage"
        ]
    ]
    .sort_values(
        "data_analyst_advantage",
        ascending=False
    )
    .head(15)
    .to_string()
)


# --------------------------------------------------
# 8. Display Business Analyst differentiators
# --------------------------------------------------

print("\n===== BUSINESS ANALYST DIFFERENTIATORS =====")

print(
    pivot[
        pivot["data_analyst_advantage"] < 0
    ][
        [
            "Data Analyst",
            "Business Analyst",
            "data_analyst_advantage"
        ]
    ]
    .sort_values(
        "data_analyst_advantage"
    )
    .head(15)
    .to_string()
)


print("\nSaved to:")
print(
    "data/processed/role_differentiation.csv"
)