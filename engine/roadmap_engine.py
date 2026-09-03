class RoadmapEngine:

    SKILL_PLANS = {

        "SQL": {
            "foundation": [
                "SELECT, WHERE and ORDER BY",
                "GROUP BY and aggregate functions",
                "JOINS and subqueries"
            ],
            "application": [
                "CTEs and window functions",
                "CASE statements",
                "Query optimization"
            ],
            "project": "Build a SQL business analytics project using a real-world dataset."
        },

        "Python": {
            "foundation": [
                "Python syntax and data types",
                "Lists, dictionaries and functions",
                "File handling"
            ],
            "application": [
                "Pandas and NumPy",
                "Data cleaning",
                "Exploratory data analysis"
            ],
            "project": "Build a Python data analysis project with a cleaned dataset and business insights."
        },

        "Tableau": {
            "foundation": [
                "Dimensions and measures",
                "Charts and filters",
                "Basic dashboards"
            ],
            "application": [
                "Calculated fields",
                "Interactive dashboards",
                "Dashboard storytelling"
            ],
            "project": "Build an interactive Tableau dashboard from a business dataset."
        },

        "Power BI": {
            "foundation": [
                "Importing and cleaning data",
                "Basic visualizations",
                "Filters and slicers"
            ],
            "application": [
                "Data modeling",
                "DAX fundamentals",
                "Interactive dashboards"
            ],
            "project": "Build a Power BI business intelligence dashboard."
        },

        "Excel": {
            "foundation": [
                "Formulas and functions",
                "Sorting and filtering",
                "Basic charts"
            ],
            "application": [
                "Pivot tables",
                "XLOOKUP and advanced formulas",
                "Data cleaning"
            ],
            "project": "Build an Excel business analysis dashboard."
        },

        "R": {
            "foundation": [
                "R syntax",
                "Vectors and data frames",
                "Basic statistical functions"
            ],
            "application": [
                "Data manipulation",
                "Statistical analysis",
                "Data visualization"
            ],
            "project": "Build a statistical analysis project using R."
        },

        "Data Visualization": {
            "foundation": [
                "Chart selection",
                "Visual hierarchy",
                "Basic storytelling"
            ],
            "application": [
                "Dashboard design",
                "Interactive visualizations",
                "Business storytelling"
            ],
            "project": "Create a business dashboard focused on decision-making."
        },

        "Data Analysis": {
            "foundation": [
                "Data cleaning",
                "Descriptive analysis",
                "Finding patterns"
            ],
            "application": [
                "Exploratory analysis",
                "Business questions",
                "Insight generation"
            ],
            "project": "Complete an end-to-end business data analysis."
        },

        "Statistics": {
            "foundation": [
                "Mean, median and mode",
                "Variance and standard deviation",
                "Probability basics"
            ],
            "application": [
                "Correlation",
                "Regression",
                "Hypothesis testing"
            ],
            "project": "Perform a statistical analysis on a real business dataset."
        },

        "Looker": {
            "foundation": [
                "Looker interface",
                "Dimensions and measures",
                "Basic reports"
            ],
            "application": [
                "LookML fundamentals",
                "Explores",
                "Interactive dashboards"
            ],
            "project": "Create a Looker analytics dashboard."
        },

        "Data Modeling": {
            "foundation": [
                "Tables and relationships",
                "Primary and foreign keys",
                "Normalization"
            ],
            "application": [
                "Star schema",
                "Fact and dimension tables",
                "Analytical data models"
            ],
            "project": "Design a data model for a business analytics system."
        },

        "ETL": {
            "foundation": [
                "Extract, transform and load concepts",
                "Data cleaning",
                "Data pipelines"
            ],
            "application": [
                "Pipeline design",
                "Data validation",
                "Automation"
            ],
            "project": "Build a small ETL pipeline from raw data to analytics-ready data."
        },

        "Snowflake": {
            "foundation": [
                "Snowflake architecture",
                "Databases and schemas",
                "Basic SQL"
            ],
            "application": [
                "Warehouses",
                "Data loading",
                "Performance concepts"
            ],
            "project": "Create a small Snowflake analytics warehouse."
        },

        "AWS": {
            "foundation": [
                "Cloud fundamentals",
                "AWS core services",
                "Storage concepts"
            ],
            "application": [
                "S3",
                "IAM",
                "Analytics services"
            ],
            "project": "Build a simple cloud-based data storage and analytics workflow."
        },

        "Machine Learning": {
            "foundation": [
                "Supervised vs unsupervised learning",
                "Training and testing data",
                "Feature concepts"
            ],
            "application": [
                "Regression",
                "Classification",
                "Model evaluation"
            ],
            "project": "Build a beginner machine-learning model using a real dataset."
        },

        "Data Warehousing": {
            "foundation": [
                "Warehouse concepts",
                "Fact and dimension tables",
                "Star schemas"
            ],
            "application": [
                "ETL pipelines",
                "Data integration",
                "Warehouse optimization"
            ],
            "project": "Design a small data warehouse for a business use case."
        },

        "Data Mining": {
            "foundation": [
                "Data mining concepts",
                "Pattern discovery",
                "Feature selection"
            ],
            "application": [
                "Clustering",
                "Classification",
                "Association rules"
            ],
            "project": "Perform a data mining analysis on a real dataset."
        },

        "Data Quality": {
            "foundation": [
                "Data quality dimensions",
                "Missing data",
                "Duplicate detection"
            ],
            "application": [
                "Validation rules",
                "Quality monitoring",
                "Data governance"
            ],
            "project": "Create a data quality checking workflow."
        }
    }

    def build_roadmap(self, recommendations):

        roadmap = []

        for item in recommendations[:3]:

            skill = item["canonical_skill"]

            plan = self.SKILL_PLANS.get(skill)

            if not plan:
                continue

            roadmap.append({

                "skill": skill,

                "priority": item.get(
                    "priority",
                    "Medium"
                ),

                "priority_score": round(
                    float(
                        item.get(
                            "priority_score",
                            0
                        )
                    ),
                    1
                ),

                "days_1_30": plan["foundation"],

                "days_31_60": plan["application"],

                "days_61_90": [
                    plan["project"]
                ]

            })

        return roadmap