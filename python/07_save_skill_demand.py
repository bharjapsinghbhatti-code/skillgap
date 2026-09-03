import pandas as pd

# Load raw datasets
vacancies = pd.read_csv("data/raw/vacancies_rows.csv")
skills = pd.read_csv("data/raw/skills_rows.csv")
vacancy_skills = pd.read_csv("data/raw/vacancy_skills_rows.csv")


# Connect job-skill relationships with skill names
skill_data = vacancy_skills.merge(
    skills,
    left_on="skill_id",
    right_on="id",
    how="left"
)


# Count unique jobs mentioning each skill
skill_demand = (
    skill_data
    .groupby("name")["vacancy_id"]
    .nunique()
    .reset_index(name="job_count")
)


# Total number of unique jobs
total_jobs = vacancies["id"].nunique()


# Calculate demand percentage
skill_demand["demand_percentage"] = (
    skill_demand["job_count"] / total_jobs * 100
)


# Sort by demand
skill_demand = skill_demand.sort_values(
    "job_count",
    ascending=False
)


# Save processed dataset
skill_demand.to_csv(
    "data/processed/skill_demand.csv",
    index=False
)


print("Skill demand dataset created successfully.")

print("\nSaved to:")
print("data/processed/skill_demand.csv")

print("\nTop 20 skills:")
print(
    skill_demand
    .head(20)
    .to_string(index=False)
)