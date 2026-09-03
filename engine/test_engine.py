from recommendation_engine import SkillGapEngine


# --------------------------------------------------
# Create engine
# --------------------------------------------------

engine = SkillGapEngine()


# --------------------------------------------------
# Test user proficiency
#
# 0 = Don't know
# 1 = Beginner
# 2 = Intermediate
# 3 = Advanced
# --------------------------------------------------

current_skills = {
    "SQL": 3,
    "Excel": 3,
    "Python": 1,
    "Power BI": 0,
    "Tableau": 2
}


# --------------------------------------------------
# Generate recommendations
# --------------------------------------------------

results = engine.recommend(
    current_skills=current_skills,
    current_level="Entry",
    target_level="Senior"
)


# --------------------------------------------------
# Core
# --------------------------------------------------

print("\n==============================")
print("CORE SKILLS")
print("==============================")

print(
    results["core"][
        [
            "canonical_skill",
            "priority_score"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# Growth
# --------------------------------------------------

print("\n==============================")
print("GROWTH SKILLS")
print("==============================")

print(
    results["growth"][
        [
            "canonical_skill",
            "priority_score"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# Specialized
# --------------------------------------------------

print("\n==============================")
print("SPECIALIZED SKILLS")
print("==============================")

print(
    results["specialized"][
        [
            "canonical_skill",
            "priority_score"
        ]
    ].to_string(index=False)
)