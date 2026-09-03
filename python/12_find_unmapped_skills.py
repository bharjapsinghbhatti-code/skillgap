import pandas as pd


# Load raw skill data
skills = pd.read_csv(
    "data/raw/skills_rows.csv"
)

# Load current taxonomy
taxonomy = pd.read_csv(
    "data/processed/skill_taxonomy_rules_v2.csv"
)

# Load skill demand
skill_demand = pd.read_csv(
    "data/processed/skill_demand.csv"
)


# Find skills already mapped
mapped_skills = set(
    taxonomy["raw_skill"]
)


# Keep only unmapped skills
unmapped = skill_demand[
    ~skill_demand["name"].isin(mapped_skills)
].copy()


# Sort by number of jobs
unmapped = unmapped.sort_values(
    "job_count",
    ascending=False
)


print("===== TOP UNMAPPED SKILLS =====")

print(
    unmapped
    .head(50)
    .to_string(index=False)
)