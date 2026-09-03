import pandas as pd

vacancies = pd.read_csv("data/raw/vacancies_rows.csv")
skills = pd.read_csv("data/raw/skills_rows.csv")
vacancy_skills = pd.read_csv("data/raw/vacancy_skills_rows.csv")


print("===== DATA QUALITY CHECK =====")


# 1. Check whether every vacancy-skill relationship
# points to a real vacancy

invalid_vacancies = vacancy_skills[
    ~vacancy_skills["vacancy_id"].isin(vacancies["id"])
]

print("\nInvalid vacancy IDs:", len(invalid_vacancies))


# 2. Check whether every vacancy-skill relationship
# points to a real skill

invalid_skills = vacancy_skills[
    ~vacancy_skills["skill_id"].isin(skills["id"])
]

print("Invalid skill IDs:", len(invalid_skills))


# 3. Check duplicate skill IDs

print(
    "Duplicate skill IDs:",
    skills["id"].duplicated().sum()
)


# 4. Check duplicate vacancy-skill relationships

print(
    "Duplicate vacancy-skill pairs:",
    vacancy_skills.duplicated().sum()
)


# 5. Check duplicate skill names

print(
    "Duplicate skill names:",
    skills["name"].duplicated().sum()
)