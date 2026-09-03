import pandas as pd

vacancies = pd.read_csv("data/raw/vacancies_rows.csv")
skills = pd.read_csv("data/raw/skills_rows.csv")
vacancy_skills = pd.read_csv("data/raw/vacancy_skills_rows.csv")

print("===== VACANCIES =====")
print("Rows:", vacancies.shape[0])
print("Columns:", vacancies.shape[1])
print(vacancies.columns.tolist())

print("\n===== SKILLS =====")
print("Rows:", skills.shape[0])
print("Columns:", skills.shape[1])
print(skills.columns.tolist())

print("\n===== VACANCY-SKILLS =====")
print("Rows:", vacancy_skills.shape[0])
print("Columns:", vacancy_skills.shape[1])
print(vacancy_skills.columns.tolist())