import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

input_file = DATA_DIR / "covid_demo_data.csv"
output_file = DATA_DIR / "covid_cleaned.csv"

# Load the sample dataset
df = pd.read_csv(input_file)

# Convert date column to date format
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Remove duplicate records and rows without essential information
df = df.drop_duplicates()
df = df.dropna(subset=["date", "location"])

# Fill missing numeric values with zero
numeric_columns = [
    "population",
    "new_cases",
    "total_cases",
    "new_deaths",
    "total_deaths",
    "people_vaccinated",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

# Calculate additional metrics
df["cases_per_million"] = (
    df["total_cases"] / df["population"].replace(0, float("nan"))
) * 1_000_000

df["case_fatality_ratio"] = (
    df["total_deaths"] / df["total_cases"].replace(0, float("nan"))
) * 100

# Sort records by country and date
df = df.sort_values(["location", "date"])

# Save cleaned data
df.to_csv(output_file, index=False)

print("Data cleaning completed!")
print(f"Rows in cleaned dataset: {len(df)}")
print(f"Saved to: {output_file}")