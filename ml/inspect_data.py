import pandas as pd

# Load dataset
df = pd.read_csv("data/revenue_recovery_dataset.csv")

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== RECOVERY DISTRIBUTION ==========")
print(df["recovered"].value_counts())

print("\n========== RECOVERY PERCENTAGE ==========")
print(df["recovered"].value_counts(normalize=True) * 100)

print("\n========== NUMERICAL SUMMARY ==========")
print(df.describe())