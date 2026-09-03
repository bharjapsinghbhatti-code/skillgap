import pandas as pd


# --------------------------------------------------
# 1. Load vacancies
# --------------------------------------------------

vacancies = pd.read_csv(
    "data/raw/vacancies_rows.csv"
)


# --------------------------------------------------
# 2. Prepare titles
# --------------------------------------------------

titles = (
    vacancies["title"]
    .fillna("")
    .str.lower()
    .str.strip()
)


vacancies["role_family"] = "Other Analytics"


# --------------------------------------------------
# 3. Business Analyst
# --------------------------------------------------

vacancies.loc[
    titles.str.contains(
        r"business analyst|business data analyst",
        regex=True
    ),
    "role_family"
] = "Business Analyst"


# --------------------------------------------------
# 4. BI Analyst
# --------------------------------------------------

vacancies.loc[
    titles.str.contains(
        r"\bbi analyst\b|business intelligence analyst|bi developer",
        regex=True
    ),
    "role_family"
] = "BI Analyst"


# --------------------------------------------------
# 5. Data Scientist
# --------------------------------------------------

vacancies.loc[
    titles.str.contains(
        r"data scientist|machine learning scientist",
        regex=True
    ),
    "role_family"
] = "Data Scientist"


# --------------------------------------------------
# 6. Data Analyst
# --------------------------------------------------

vacancies.loc[
    titles.str.contains(
        r"(?<!business )\bdata analyst\b",
        regex=True
    ),
    "role_family"
] = "Data Analyst"

# --------------------------------------------------
# 7. Save
# --------------------------------------------------

vacancies.to_csv(
    "data/processed/vacancies_with_roles.csv",
    index=False
)


# --------------------------------------------------
# 8. Distribution
# --------------------------------------------------

print("===== ROLE FAMILY DISTRIBUTION =====")

print(
    vacancies["role_family"]
    .value_counts()
)


# --------------------------------------------------
# 9. Show examples
# --------------------------------------------------

print("\n===== ROLE EXAMPLES =====")

for role in vacancies["role_family"].unique():

    print(f"\n--- {role} ---")

    print(
        vacancies.loc[
            vacancies["role_family"] == role,
            "title"
        ]
        .drop_duplicates()
        .head(10)
        .to_string(index=False)
    )


print("\nSaved to:")
print(
    "data/processed/vacancies_with_roles.csv"
)