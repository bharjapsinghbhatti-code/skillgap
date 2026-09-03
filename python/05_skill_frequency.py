import pandas as pd

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


# Count how many jobs mention each skill
skill_frequency = (
    skill_data
    .groupby("name")["vacancy_id"]
    .nunique()
    .sort_values(ascending=False)
)


print("===== TOP 50 SKILLS =====")

print(
    skill_frequency
    .head(50)
    .to_string()
)