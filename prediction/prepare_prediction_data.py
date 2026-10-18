import pandas as pd
from pathlib import Path

# ---------------------------------------
# AURA-Edge: Prediction Dataset Preparation
# ---------------------------------------

INPUT_FILE = Path(
    "data/processed/machine_usage_clean.csv"
)

OUTPUT_FILE = Path(
    "data/processed/prediction_dataset.csv"
)

print("Loading processed Alibaba data...")

df = pd.read_csv(INPUT_FILE)

# Sort by machine and time
df = df.sort_values(
    ["machine_id", "timestamp"]
).reset_index(drop=True)

print("Rows loaded:", len(df))
print("Machines:", df["machine_id"].nunique())

# ---------------------------------------
# Create historical CPU features
# ---------------------------------------

# Previous 5 CPU utilization values
for i in range(1, 6):
    df[f"cpu_lag_{i}"] = (
        df.groupby("machine_id")["cpu_util_percent"]
        .shift(i)
    )

# ---------------------------------------
# Prediction target
# ---------------------------------------

# Predict the next CPU utilization value
df["target_cpu"] = (
    df.groupby("machine_id")["cpu_util_percent"]
    .shift(-1)
)

# ---------------------------------------
# Remove rows where history/target
# is not available
# ---------------------------------------

feature_columns = [
    "cpu_lag_1",
    "cpu_lag_2",
    "cpu_lag_3",
    "cpu_lag_4",
    "cpu_lag_5",
]

df = df.dropna(
    subset=feature_columns + ["target_cpu"]
)

# Keep only columns needed for prediction
prediction_df = df[
    [
        "machine_id",
        "timestamp",
        "cpu_lag_1",
        "cpu_lag_2",
        "cpu_lag_3",
        "cpu_lag_4",
        "cpu_lag_5",
        "target_cpu",
    ]
]

# ---------------------------------------
# Save prediction dataset
# ---------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

prediction_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nPrediction dataset created successfully!")

print("Rows:", len(prediction_df))
print("Columns:", list(prediction_df.columns))

print("\nFirst 5 rows:")
print(prediction_df.head())

print("\nSaved to:")
print(OUTPUT_FILE)