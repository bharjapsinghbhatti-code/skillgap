import pandas as pd


# Load datasets
vacancies = pd.read_csv(
    "data/raw/vacancies_rows.csv"
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
# 1. Connect jobs to raw skill names
# --------------------------------------------------

job_skills = vacancy_skills.merge(
    skills,
    left_on="skill_id",
    right_on="id",
    how="left"
)


# --------------------------------------------------
# 2. Apply our taxonomy
# --------------------------------------------------

job_skills = job_skills.merge(
    taxonomy,
    left_on="name",
    right_on="raw_skill",
    how="inner"
)


# --------------------------------------------------
# 3. Add experience information
# --------------------------------------------------

job_skills = job_skills.merge(
    vacancies[
        ["id", "experience_level"]
    ],
    left_on="vacancy_id",
    right_on="id",
    how="left"
)


# --------------------------------------------------
# 4. Remove missing experience levels
# --------------------------------------------------

job_skills = job_skills[
    job_skills["experience_level"].notna()
]


# --------------------------------------------------
# 5. Count unique jobs by experience + skill
# --------------------------------------------------

experience_skill = (
    job_skills
    .groupby(
        [
            "experience_level",
            "canonical_skill",
            "category"
        ]
    )["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# --------------------------------------------------
# 6. Count total jobs at each experience level
# --------------------------------------------------

experience_totals = (
    vacancies[
        vacancies["experience_level"].notna()
    ]
    .groupby("experience_level")["id"]
    .nunique()
    .reset_index(name="total_jobs")
)


# --------------------------------------------------
# 7. Merge totals
# --------------------------------------------------

experience_skill = experience_skill.merge(
    experience_totals,
    on="experience_level",
    how="left"
)


# --------------------------------------------------
# 8. Calculate percentage within each level
# --------------------------------------------------

experience_skill["demand_percentage"] = (
    experience_skill["job_count"]
    / experience_skill["total_jobs"]
    * 100
)


# --------------------------------------------------
# 9. Sort
# --------------------------------------------------

experience_skill = experience_skill.sort_values(
    [
        "experience_level",
        "job_count"
    ],
    ascending=[True, False]
)


# --------------------------------------------------
# 10. Save
# --------------------------------------------------

experience_skill.to_csv(
    "data/processed/skill_demand_by_experience.csv",
    index=False
)


print("===== SKILL DEMAND BY EXPERIENCE =====")

print(
    experience_skill
    .to_string(index=False)
)

print("\nSaved to:")
print(
    "data/processed/skill_demand_by_experience.csv"
)