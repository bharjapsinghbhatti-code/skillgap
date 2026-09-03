import pandas as pd


# Load raw data
skills = pd.read_csv(
    "data/raw/skills_rows.csv"
)

vacancy_skills = pd.read_csv(
    "data/raw/vacancy_skills_rows.csv"
)

vacancies = pd.read_csv(
    "data/raw/vacancies_rows.csv"
)


# Load our taxonomy rules
taxonomy = pd.read_csv(
    "data/processed/skill_taxonomy_rules_v2.csv"
)


# Connect jobs to skill names
job_skills = vacancy_skills.merge(
    skills,
    left_on="skill_id",
    right_on="id",
    how="left"
)


# Apply taxonomy
mapped_jobs = job_skills.merge(
    taxonomy,
    left_on="name",
    right_on="raw_skill",
    how="inner"
)


# Count unique jobs for each canonical skill
canonical_demand = (
    mapped_jobs
    .groupby(
        [
            "canonical_skill",
            "category",
            "subcategory",
            "skill_type"
        ]
    )["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# Calculate percentage
total_jobs = vacancies["id"].nunique()

canonical_demand["demand_percentage"] = (
    canonical_demand["job_count"]
    / total_jobs
    * 100
)


# Sort
canonical_demand = canonical_demand.sort_values(
    "job_count",
    ascending=False
)


# Save
canonical_demand.to_csv(
    "data/processed/canonical_skill_demand_v2.csv",
    index=False
)


print("===== TAXONOMY V2 APPLIED =====")

print(
    canonical_demand
    .to_string(index=False)
)

print("\nSaved to:")
print(
    "data/processed/canonical_skill_demand_v2.csv"
)