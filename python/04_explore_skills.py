import pandas as pd

skills = pd.read_csv("data/raw/skills_rows.csv")


print("===== SKILL DATASET =====")

print("Total skills:", len(skills))


print("\n===== FIRST 100 SKILLS =====")

print(
    skills["name"]
    .head(100)
    .to_string(index=False)
)


print("\n===== SKILLS CONTAINING SQL =====")

sql_skills = skills[
    skills["name"]
    .str.contains("sql", case=False, na=False)
]

print(
    sql_skills["name"]
    .to_string(index=False)
)


print("\n===== SKILLS CONTAINING EXCEL =====")

excel_skills = skills[
    skills["name"]
    .str.contains("excel", case=False, na=False)
]

print(
    excel_skills["name"]
    .to_string(index=False)
)


print("\n===== SKILLS CONTAINING POWER BI =====")

powerbi_skills = skills[
    skills["name"]
    .str.contains("power bi", case=False, na=False)
]

print(
    powerbi_skills["name"]
    .to_string(index=False)
)