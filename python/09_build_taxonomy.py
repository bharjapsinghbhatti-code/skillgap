import pandas as pd

# Load the raw skills
skills = pd.read_csv("data/raw/skills_rows.csv")


# --------------------------------------------------
# 1. Define our manually validated mappings
# --------------------------------------------------

taxonomy_rules = {

    # Excel
    "Excel": {
        "canonical": "Excel",
        "category": "BI & Reporting",
        "subcategory": "Spreadsheets",
        "mapping_type": "Core"
    },

    "Microsoft Excel": {
        "canonical": "Excel",
        "category": "BI & Reporting",
        "subcategory": "Spreadsheets",
        "mapping_type": "Alias"
    },

    "MS Excel": {
        "canonical": "Excel",
        "category": "BI & Reporting",
        "subcategory": "Spreadsheets",
        "mapping_type": "Alias"
    },


    # Power BI
    "Power BI": {
        "canonical": "Power BI",
        "category": "BI & Reporting",
        "subcategory": "BI Tools",
        "mapping_type": "Core"
    },

    "Microsoft Power BI": {
        "canonical": "Power BI",
        "category": "BI & Reporting",
        "subcategory": "BI Tools",
        "mapping_type": "Alias"
    },


    # SQL
    "SQL": {
        "canonical": "SQL",
        "category": "Data & Analytics",
        "subcategory": "Query Languages",
        "mapping_type": "Core"
    },

    "Advanced SQL": {
        "canonical": "SQL",
        "category": "Data & Analytics",
        "subcategory": "Query Languages",
        "mapping_type": "Variant"
    },

    "T-SQL": {
        "canonical": "SQL",
        "category": "Data & Analytics",
        "subcategory": "Query Languages",
        "mapping_type": "Variant"
    },

    "MS SQL": {
        "canonical": "SQL",
        "category": "Data & Analytics",
        "subcategory": "Query Languages",
        "mapping_type": "Variant"
    },

    "MSSQL": {
        "canonical": "SQL",
        "category": "Data & Analytics",
        "subcategory": "Query Languages",
        "mapping_type": "Variant"
    },


    # Python
    "Python": {
        "canonical": "Python",
        "category": "Programming & Data",
        "subcategory": "Programming Languages",
        "mapping_type": "Core"
    },


    # Tableau
    "Tableau": {
        "canonical": "Tableau",
        "category": "BI & Reporting",
        "subcategory": "BI Tools",
        "mapping_type": "Core"
    },

    "Tableau Server": {
        "canonical": "Tableau",
        "category": "BI & Reporting",
        "subcategory": "BI Tools",
        "mapping_type": "Variant"
    },

    "Tableau Prep": {
        "canonical": "Tableau",
        "category": "BI & Reporting",
        "subcategory": "BI Tools",
        "mapping_type": "Variant"
    },


    # Analytics
    "Data Analysis": {
        "canonical": "Data Analysis",
        "category": "Data & Analytics",
        "subcategory": "Analysis",
        "mapping_type": "Core"
    },

    "Data analysis": {
        "canonical": "Data Analysis",
        "category": "Data & Analytics",
        "subcategory": "Analysis",
        "mapping_type": "Alias"
    },

    "Data Visualization": {
        "canonical": "Data Visualization",
        "category": "Data & Analytics",
        "subcategory": "Visualization",
        "mapping_type": "Core"
    },

    "Data visualization": {
        "canonical": "Data Visualization",
        "category": "Data & Analytics",
        "subcategory": "Visualization",
        "mapping_type": "Alias"
    },

    "Data Visualization Tools": {
        "canonical": "Data Visualization",
        "category": "Data & Analytics",
        "subcategory": "Visualization",
        "mapping_type": "Variant"
    },


    # Statistics
    "Statistics": {
        "canonical": "Statistics",
        "category": "Data & Analytics",
        "subcategory": "Statistics",
        "mapping_type": "Core"
    },

    "Statistical Analysis": {
        "canonical": "Statistics",
        "category": "Data & Analytics",
        "subcategory": "Statistics",
        "mapping_type": "Variant"
    },

    "Descriptive Statistics": {
        "canonical": "Statistics",
        "category": "Data & Analytics",
        "subcategory": "Statistics",
        "mapping_type": "Variant"
    },

    "Inferential Statistics": {
        "canonical": "Statistics",
        "category": "Data & Analytics",
        "subcategory": "Statistics",
        "mapping_type": "Variant"
    }
}


# --------------------------------------------------
# 2. Create the taxonomy dataframe
# --------------------------------------------------

taxonomy_rows = []

for _, row in skills.iterrows():

    raw_skill = row["name"]

    if raw_skill in taxonomy_rules:

        rule = taxonomy_rules[raw_skill]

        taxonomy_rows.append({
            "raw_skill": raw_skill,
            "canonical_skill": rule["canonical"],
            "category": rule["category"],
            "subcategory": rule["subcategory"],
            "mapping_type": rule["mapping_type"],
            "confidence": "High"
        })


# --------------------------------------------------
# 3. Convert to DataFrame
# --------------------------------------------------

taxonomy = pd.DataFrame(taxonomy_rows)


# --------------------------------------------------
# 4. Save
# --------------------------------------------------

taxonomy.to_csv(
    "data/processed/skill_taxonomy_v1.csv",
    index=False
)


print("===== TAXONOMY CREATED =====")

print("Mapped skills:", len(taxonomy))

print("\nSaved to:")
print("data/processed/skill_taxonomy_v1.csv")

print("\nPreview:")
print(taxonomy.head(20).to_string(index=False))