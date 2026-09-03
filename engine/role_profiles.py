# =========================================================
# SkillGap - Role Skill Profiles
# =========================================================

ROLE_PROFILES = {

    "Data Analyst": {

        "SQL": 1.00,
        "Excel": 0.90,
        "Data Analysis": 1.00,
        "Data Visualization": 0.90,
        "Power BI": 0.85,
        "Tableau": 0.80,
        "Python": 0.80,
        "Statistics": 0.75,
        "R": 0.35,

        "Looker": 0.50,
        "Data Modeling": 0.65,
        "ETL": 0.55,
        "Snowflake": 0.45,

        "AWS": 0.25,
        "Machine Learning": 0.30,
        "Data Warehousing": 0.45,
        "Data Mining": 0.35,
        "Data Quality": 0.60
    },


    "Business Analyst": {

        "Excel": 1.00,
        "Data Analysis": 0.95,
        "SQL": 0.80,
        "Power BI": 0.85,
        "Tableau": 0.75,
        "Data Visualization": 0.80,
        "Statistics": 0.65,
        "Python": 0.55,
        "R": 0.25,

        "Looker": 0.40,
        "Data Modeling": 0.55,
        "ETL": 0.40,
        "Snowflake": 0.25,

        "AWS": 0.15,
        "Machine Learning": 0.15,
        "Data Warehousing": 0.30,
        "Data Mining": 0.20,
        "Data Quality": 0.45
    },


    "BI Analyst": {

        "Power BI": 1.00,
        "Tableau": 0.95,
        "SQL": 0.90,
        "Data Visualization": 1.00,
        "Data Analysis": 0.90,
        "Excel": 0.85,
        "Data Modeling": 0.80,
        "ETL": 0.70,
        "Python": 0.60,
        "Statistics": 0.60,
        "R": 0.25,

        "Looker": 0.65,
        "Snowflake": 0.55,

        "AWS": 0.30,
        "Machine Learning": 0.20,
        "Data Warehousing": 0.65,
        "Data Mining": 0.25,
        "Data Quality": 0.55
    },


    "Data Scientist": {

        "Python": 1.00,
        "Statistics": 1.00,
        "Machine Learning": 1.00,
        "Data Analysis": 0.95,
        "SQL": 0.85,
        "Data Mining": 0.85,
        "R": 0.70,
        "Data Visualization": 0.70,
        "Tableau": 0.45,
        "Power BI": 0.40,
        "Excel": 0.35,

        "Data Modeling": 0.80,
        "ETL": 0.55,
        "Snowflake": 0.50,
        "Looker": 0.30,

        "AWS": 0.60,
        "Data Warehousing": 0.55,
        "Data Quality": 0.55
    },


    "Marketing Analyst": {

        "Excel": 0.95,
        "Data Analysis": 1.00,
        "Statistics": 0.75,
        "Data Visualization": 0.85,
        "SQL": 0.70,
        "Tableau": 0.70,
        "Power BI": 0.65,
        "Python": 0.55,
        "R": 0.25,

        "Looker": 0.45,
        "Data Modeling": 0.35,
        "ETL": 0.30,
        "Snowflake": 0.20,

        "AWS": 0.10,
        "Machine Learning": 0.35,
        "Data Warehousing": 0.20,
        "Data Mining": 0.55,
        "Data Quality": 0.40
    },


    "Financial Analyst": {

        "Excel": 1.00,
        "Data Analysis": 0.95,
        "Statistics": 0.80,
        "SQL": 0.70,
        "Data Visualization": 0.75,
        "Power BI": 0.70,
        "Tableau": 0.60,
        "Python": 0.55,
        "R": 0.30,

        "Data Modeling": 0.50,
        "ETL": 0.30,
        "Snowflake": 0.20,
        "Looker": 0.25,

        "AWS": 0.10,
        "Machine Learning": 0.20,
        "Data Warehousing": 0.25,
        "Data Mining": 0.35,
        "Data Quality": 0.45
    }
}


# =========================================================
# DEFAULT PROFILE
# =========================================================

DEFAULT_ROLE_PROFILE = {

    "SQL": 0.50,
    "Excel": 0.50,
    "Python": 0.50,
    "Tableau": 0.50,
    "Power BI": 0.50,
    "R": 0.30,
    "Data Visualization": 0.50,
    "Data Analysis": 0.50,
    "Statistics": 0.50,

    "Looker": 0.30,
    "Data Modeling": 0.40,
    "ETL": 0.30,
    "Snowflake": 0.25,

    "AWS": 0.20,
    "Machine Learning": 0.20,
    "Data Warehousing": 0.30,
    "Data Mining": 0.25,
    "Data Quality": 0.40
}


# =========================================================
# GET ROLE PROFILE
# =========================================================

def get_role_profile(role: str) -> dict:

    profile = ROLE_PROFILES.get(role)

    if profile is None:
        return DEFAULT_ROLE_PROFILE.copy()

    return profile.copy()


# =========================================================
# AVAILABLE ROLES
# =========================================================

def get_available_roles() -> list[str]:

    return list(ROLE_PROFILES.keys())