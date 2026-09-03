import pandas as pd

vacancies = pd.read_csv("data/raw/vacancies_rows.csv")
skills = pd.read_csv("data/raw/skills_rows.csv")
vacancy_skills = pd.read_csv("data/raw/vacancy_skills_rows.csv")


# Connect job-skill relationships to skill names
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


# Calculate percentage of all jobs
total_jobs = vacancies["id"].nunique()

skill_demand["demand_percentage"] = (
    skill_demand["job_count"] / total_jobs * 100
)


# Sort from highest demand to lowest
skill_demand = skill_demand.sort_values(
    "job_count",
    ascending=False
)


print("===== TOP 50 SKILLS BY MARKET DEMAND =====")

print(
    skill_demand
    .head(50)
    .to_string(index=False)
)