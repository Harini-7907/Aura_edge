import pandas as pd
from pathlib import Path

# Input Alibaba resource data
INPUT_FILE = Path(
    "data/processed/machine_usage_clean.csv"
)

# Output resource prediction dataset
OUTPUT_FILE = Path(
    "data/processed/resource_prediction_dataset.csv"
)

print("Loading Alibaba machine resource data...")

df = pd.read_csv(INPUT_FILE)

print("Rows loaded:", len(df))
print("Machines:", df["machine_id"].nunique())

# Sort data by machine and time
df = df.sort_values(
    ["machine_id", "timestamp"]
).reset_index(drop=True)

print("\nCreating resource history features...")

# Resources we want to predict
resources = {
    "cpu_util_percent": "cpu",
    "mem_util_percent": "memory",
    "net_in": "net_in",
    "net_out": "net_out",
    "disk_io_percent": "disk"
}

# Create 5 previous observations for each resource
for column, prefix in resources.items():

    for i in range(1, 6):

        df[f"{prefix}_lag_{i}"] = (
            df.groupby("machine_id")[column].shift(i)
        )

print("Creating future resource targets...")

# Create next-step target for each resource
for column, prefix in resources.items():

    df[f"target_{prefix}"] = (
        df.groupby("machine_id")[column].shift(-1)
    )

print("Removing incomplete rows...")

# All historical features
feature_columns = []

for prefix in resources.values():

    for i in range(1, 6):

        feature_columns.append(
            f"{prefix}_lag_{i}"
        )

# All prediction targets
target_columns = [
    "target_cpu",
    "target_memory",
    "target_net_in",
    "target_net_out",
    "target_disk"
]

# ==========================================
# CLEAN INVALID DISK VALUES
# ==========================================

print("\nCleaning invalid disk values...")

disk_columns = [
    "disk_lag_1",
    "disk_lag_2",
    "disk_lag_3",
    "disk_lag_4",
    "disk_lag_5",
    "target_disk"
]

for column in disk_columns:

    df[column] = df[column].replace(
        [-1, 101],
        pd.NA
    )


# ==========================================
# REMOVE INCOMPLETE ROWS
# ==========================================

print("Removing incomplete rows...")

df = df.dropna(
    subset=feature_columns + target_columns
)

# Select final columns
prediction_df = df[
    ["machine_id", "timestamp"]
    + feature_columns
    + target_columns
]

# Make sure output folder exists
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save dataset
prediction_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n==========================================")
print("RESOURCE PREDICTION DATASET CREATED")
print("==========================================")

print("Rows:", len(prediction_df))
print("Machines:", prediction_df["machine_id"].nunique())

print("\nFirst 5 rows:")
print(prediction_df.head())

print("\nSaved to:")
print(OUTPUT_FILE)