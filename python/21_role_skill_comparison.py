import pandas as pd


# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

vacancies = pd.read_csv(
    "data/processed/vacancies_with_roles.csv"
)

skills = pd.read_csv(
    "data/raw/skills_rows.csv"
)

vacancy_skills = pd.read_csv(
    "data/raw/vacancy_skills_rows.csv"
)

taxonomy = pd.read_csv(
    "data/processed/skill_taxonomy_rules_v2.csv"
)


# --------------------------------------------------
# 2. Keep only roles with enough data
# --------------------------------------------------

valid_roles = [
    "Data Analyst",
    "Business Analyst"
]

vacancies = vacancies[
    vacancies["role_family"].isin(valid_roles)
]


# --------------------------------------------------
# 3. Connect jobs to raw skills
# --------------------------------------------------

job_skills = vacancy_skills.merge(
    skills,
    left_on="skill_id",
    right_on="id",
    how="left"
)


# --------------------------------------------------
# 4. Apply taxonomy
# --------------------------------------------------

job_skills = job_skills.merge(
    taxonomy,
    left_on="name",
    right_on="raw_skill",
    how="inner"
)


# --------------------------------------------------
# 5. Add role family
# --------------------------------------------------

job_skills = job_skills.merge(
    vacancies[
        ["id", "role_family"]
    ],
    left_on="vacancy_id",
    right_on="id",
    how="inner"
)


# --------------------------------------------------
# 6. Count unique jobs per role + skill
# --------------------------------------------------

role_skill = (
    job_skills
    .groupby(
        [
            "role_family",
            "canonical_skill",
            "category"
        ]
    )["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# --------------------------------------------------
# 7. Get total jobs per role
# --------------------------------------------------

role_totals = (
    vacancies
    .groupby("role_family")["id"]
    .nunique()
    .reset_index(name="total_jobs")
)


# --------------------------------------------------
# 8. Calculate role-specific demand
# --------------------------------------------------

role_skill = role_skill.merge(
    role_totals,
    on="role_family",
    how="left"
)

role_skill["demand_percentage"] = (
    role_skill["job_count"]
    / role_skill["total_jobs"]
    * 100
)


# --------------------------------------------------
# 9. Save detailed results
# --------------------------------------------------

role_skill.to_csv(
    "data/processed/role_skill_demand.csv",
    index=False
)


# --------------------------------------------------
# 10. Display top skills for each role
# --------------------------------------------------

for role in valid_roles:

    print("\n===================================")
    print(role.upper())
    print("===================================")

    result = role_skill[
        role_skill["role_family"] == role
    ].sort_values(
        "demand_percentage",
        ascending=False
    )

    print(
        result[
            [
                "canonical_skill",
                "category",
                "job_count",
                "demand_percentage"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


print("\nSaved to:")
print(
    "data/processed/role_skill_demand.csv"
)