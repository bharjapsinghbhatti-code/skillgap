import pandas as pd

# Load our three datasets
vacancies = pd.read_csv("data/raw/vacancies_rows.csv")
skills = pd.read_csv("data/raw/skills_rows.csv")
vacancy_skills = pd.read_csv("data/raw/vacancy_skills_rows.csv")


print("\n===== BASIC INFORMATION =====")

print("Number of jobs:", len(vacancies))
print("Number of skills:", len(skills))
print("Number of job-skill relationships:", len(vacancy_skills))


print("\n===== JOB TITLES =====")

print(vacancies["title"].value_counts().head(20))


print("\n===== EXPERIENCE LEVELS =====")

print(vacancies["experience_level"].value_counts(dropna=False))


print("\n===== LOCATIONS =====")

print(vacancies["location"].value_counts().head(20))


print("\n===== DATE RANGE =====")

print("Oldest posting:", vacancies["published_at"].min())
print("Newest posting:", vacancies["published_at"].max())


print("\n===== MISSING VALUES =====")

print(vacancies.isnull().sum())


print("\n===== DUPLICATES =====")

print("Duplicate job IDs:", vacancies["id"].duplicated().sum())


print("\n===== SAMPLE SKILLS =====")

print(skills["name"].head(30).to_string(index=False))