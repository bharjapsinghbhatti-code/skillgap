import pandas as pd


# Load vacancies
vacancies = pd.read_csv(
    "data/raw/vacancies_rows.csv"
)


# --------------------------------------------------
# Map raw experience labels to standardized levels
# --------------------------------------------------

experience_map = {

    "Internship": "Internship",

    "Entry level": "Entry",

    "Associate": "Entry",

    "Junior": "Junior",

    "Middle": "Mid",

    "Mid-Senior level": "Mid-Senior",

    "Senior": "Senior",

    "Lead": "Lead",

    "Not Applicable": "Unknown",

    "Not specified": "Unknown"
}


vacancies["standard_experience_level"] = (
    vacancies["experience_level"]
    .map(experience_map)
)


# --------------------------------------------------
# Check unmapped values
# --------------------------------------------------

unmapped = vacancies[
    vacancies["standard_experience_level"].isna()
]["experience_level"].unique()


print("===== EXPERIENCE LEVEL NORMALIZATION =====")

print("\nUnmapped values:")

print(unmapped)


# --------------------------------------------------
# Show distribution
# --------------------------------------------------

print("\n===== STANDARDIZED DISTRIBUTION =====")

print(
    vacancies["standard_experience_level"]
    .value_counts(dropna=False)
)


# --------------------------------------------------
# Save
# --------------------------------------------------

vacancies.to_csv(
    "data/processed/vacancies_normalized.csv",
    index=False
)


print("\nSaved to:")
print(
    "data/processed/vacancies_normalized.csv"
)