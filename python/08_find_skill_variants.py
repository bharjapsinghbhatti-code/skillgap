import pandas as pd

skills = pd.read_csv("data/raw/skills_rows.csv")


search_terms = [
    "excel",
    "sql",
    "power bi",
    "tableau",
    "python",
    "statistics",
    "data visualization",
    "data analysis",
    "machine learning",
    "cloud",
    "communication",
    "project management"
]


for term in search_terms:

    print("\n===================================")
    print(f"SKILLS RELATED TO: {term.upper()}")
    print("===================================")

    matches = skills[
        skills["name"]
        .str.contains(term, case=False, na=False)
    ]

    print(
        matches["name"]
        .to_string(index=False)
    )