import pandas as pd


# --------------------------------------------------
# 1. Load our datasets
# --------------------------------------------------

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
    "data/processed/skill_taxonomy_v1.csv"
)


# --------------------------------------------------
# 2. Connect vacancy IDs with skill names
# --------------------------------------------------

job_skills = vacancy_skills.merge(
    skills,
    left_on="skill_id",
    right_on="id",
    how="left"
)


# --------------------------------------------------
# 3. Connect raw skills to canonical skills
# --------------------------------------------------

job_skills = job_skills.merge(
    taxonomy,
    left_on="name",
    right_on="raw_skill",
    how="inner"
)


# --------------------------------------------------
# 4. Count unique jobs per canonical skill
# --------------------------------------------------

canonical_demand = (
    job_skills
    .groupby(
        [
            "canonical_skill",
            "category",
            "subcategory"
        ]
    )["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# --------------------------------------------------
# 5. Calculate market demand percentage
# --------------------------------------------------

total_jobs = vacancies["id"].nunique()

canonical_demand["demand_percentage"] = (
    canonical_demand["job_count"]
    / total_jobs
    * 100
)


# --------------------------------------------------
# 6. Sort by demand
# --------------------------------------------------

canonical_demand = canonical_demand.sort_values(
    "job_count",
    ascending=False
)


# --------------------------------------------------
# 7. Save the results
# --------------------------------------------------

canonical_demand.to_csv(
    "data/processed/canonical_skill_demand_v1.csv",
    index=False
)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("===== CANONICAL SKILL DEMAND =====")

print(
    canonical_demand
    .to_string(index=False)
)