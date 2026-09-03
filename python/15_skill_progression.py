import pandas as pd


# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

vacancies = pd.read_csv(
    "data/processed/vacancies_normalized.csv"
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
# 2. Keep only known career levels
# --------------------------------------------------

vacancies = vacancies[
    vacancies["standard_experience_level"].isin([
        "Internship",
        "Entry",
        "Junior",
        "Mid",
        "Mid-Senior",
        "Senior",
        "Lead"
    ])
]


# --------------------------------------------------
# 3. Connect jobs → raw skills
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
# 5. Connect experience levels
# --------------------------------------------------

job_skills = job_skills.merge(
    vacancies[
        ["id", "standard_experience_level"]
    ],
    left_on="vacancy_id",
    right_on="id",
    how="inner"
)


# --------------------------------------------------
# 6. Count unique jobs
# --------------------------------------------------

skill_counts = (
    job_skills
    .groupby(
        [
            "standard_experience_level",
            "canonical_skill",
            "category"
        ]
    )["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# --------------------------------------------------
# 7. Count jobs at each experience level
# --------------------------------------------------

level_totals = (
    vacancies
    .groupby("standard_experience_level")["id"]
    .nunique()
    .reset_index(name="total_jobs")
)


# --------------------------------------------------
# 8. Calculate percentage
# --------------------------------------------------

skill_counts = skill_counts.merge(
    level_totals,
    on="standard_experience_level",
    how="left"
)

skill_counts["demand_percentage"] = (
    skill_counts["job_count"]
    / skill_counts["total_jobs"]
    * 100
)


# --------------------------------------------------
# 9. Save detailed dataset
# --------------------------------------------------

skill_counts.to_csv(
    "data/processed/skill_progression.csv",
    index=False
)


# --------------------------------------------------
# 10. Create a matrix
# --------------------------------------------------

matrix = skill_counts.pivot_table(
    index="canonical_skill",
    columns="standard_experience_level",
    values="demand_percentage",
    aggfunc="first"
)


# --------------------------------------------------
# 11. Keep important skills
# --------------------------------------------------

important_skills = [
    "SQL",
    "Excel",
    "Python",
    "Tableau",
    "Power BI",
    "R",
    "Data Visualization",
    "Data Analysis",
    "Statistics",
    "Data Modeling",
    "Looker",
    "ETL",
    "Reporting",
    "Snowflake",
    "AWS",
    "Machine Learning",
    "Data Mining",
    "Data Quality",
    "Data Warehousing"
]

matrix = matrix.reindex(
    [x for x in important_skills if x in matrix.index]
)


# --------------------------------------------------
# 12. Save matrix
# --------------------------------------------------

matrix.to_csv(
    "data/processed/skill_progression_matrix.csv"
)


# --------------------------------------------------
# 13. Display
# --------------------------------------------------

print("===== SKILL PROGRESSION MATRIX =====")

print(
    matrix.to_string()
)

print("\nSaved to:")
print(
    "data/processed/skill_progression_matrix.csv"
)