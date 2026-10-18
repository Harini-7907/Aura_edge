import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "data/raw/alibaba_clusterdata_v2018/container_usage.csv"
)

OUTPUT_FILE = Path(
    "data/processed/workload_prediction_dataset.csv"
)

COLUMNS = [
    "unused",
    "instance_id",
    "timestamp",
    "cpu_util",
    "mem_util",
    "disk_util",
    "load1",
    "load5",
    "load15",
    "avg_cpi",
    "avg_mpki",
    "max_cpi"
]

print("Processing Alibaba container workload data...")

chunks = []
rows_collected = 0

for chunk in pd.read_csv(
    INPUT_FILE,
    header=None,
    names=COLUMNS,
    chunksize=100_000
):

    # Remove unused first column
    chunk = chunk.drop(
        columns=["unused"]
    )

    # Remove rows without essential identifiers
    chunk = chunk.dropna(
        subset=[
            "instance_id",
            "timestamp",
            "cpu_util",
            "mem_util"
        ]
    )

    # Keep valid utilization values
    chunk = chunk[
        (chunk["cpu_util"] >= 0) &
        (chunk["cpu_util"] <= 100) &
        (chunk["mem_util"] >= 0) &
        (chunk["mem_util"] <= 100)
    ]

    # Clean invalid disk values
    chunk["disk_util"] = chunk[
        "disk_util"
    ].replace(
        [-1, 101],
        pd.NA
    )

    # Keep rows with valid disk utilization
    chunk = chunk.dropna(
        subset=["disk_util"]
    )

    chunks.append(chunk)

    rows_collected += len(chunk)

    print(
        f"Processed {rows_collected:,} valid rows..."
    )

    if rows_collected >= 1_000_000:
        break


df = pd.concat(
    chunks,
    ignore_index=True
)

# Limit exactly to 1 million observations
df = df.iloc[:1_000_000].copy()

print("\nSorting workload data...")

df = df.sort_values(
    ["instance_id", "timestamp"]
).reset_index(drop=True)


print("\nCreating workload history features...")

workload_columns = [
    "cpu_util",
    "mem_util",
    "disk_util",
    "load1",
    "load5",
    "load15"
]

# Previous 5 observations
for column in workload_columns:

    for i in range(1, 6):

        df[f"{column}_lag_{i}"] = (
            df.groupby("instance_id")[column]
            .shift(i)
        )


print("\nCreating future workload targets...")

# Predict next workload observation
for column in workload_columns:

    df[f"target_{column}"] = (
        df.groupby("instance_id")[column]
        .shift(-1)
    )


print("\nRemoving incomplete sequences...")

feature_columns = []

for column in workload_columns:

    for i in range(1, 6):

        feature_columns.append(
            f"{column}_lag_{i}"
        )


target_columns = [
    "target_cpu_util",
    "target_mem_util",
    "target_disk_util",
    "target_load1",
    "target_load5",
    "target_load15"
]


df = df.dropna(
    subset=feature_columns + target_columns
)


# Final dataset
prediction_df = df[
    ["instance_id", "timestamp"]
    + feature_columns
    + target_columns
]


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

prediction_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n==========================================")
print("WORKLOAD PREDICTION DATASET CREATED")
print("==========================================")

print(
    "Rows:",
    len(prediction_df)
)

print(
    "Instances:",
    prediction_df["instance_id"].nunique()
)

print(
    "Columns:",
    len(prediction_df.columns)
)

print("\nColumns:")
print(
    prediction_df.columns.tolist()
)

print("\nFirst 5 rows:")
print(
    prediction_df.head()
)

print("\nMissing values:")
print(
    prediction_df.isna().sum().sum()
)

print("\nSaved to:")
print(OUTPUT_FILE)