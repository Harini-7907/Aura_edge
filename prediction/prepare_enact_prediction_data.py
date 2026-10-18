import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "node_telemetry_pods_on_clean.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "enact_prediction_dataset.csv"
)


# ==========================================
# SETTINGS
# ==========================================

LAG_STEPS = 5


# ==========================================
# LOAD ENACT DATA
# ==========================================

print("Loading ENACT telemetry...")

df = pd.read_csv(INPUT_FILE)


# ==========================================
# TIMESTAMP
# ==========================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.dropna(
    subset=["timestamp"]
)


# ==========================================
# SELECT rpi4
# ==========================================

df = df[
    df["node_name"] == "rpi4"
].copy()


# ==========================================
# SORT BY TIME
# ==========================================

df = df.sort_values(
    "timestamp"
)


# ==========================================
# REMOVE DUPLICATE TIMESTAMPS
# ==========================================

df = df.drop_duplicates(
    subset=["timestamp"],
    keep="last"
)


# ==========================================
# CONVERT FRACTIONS TO PERCENTAGES
# ==========================================

df["cpu_percent"] = (
    df["CPU (%)"] * 100
)

df["memory_percent"] = (
    df["MEM (%)"] * 100
)


# ==========================================
# SELECT REQUIRED COLUMNS
# ==========================================

data = df[
    [
        "timestamp",
        "cpu_percent",
        "memory_percent"
    ]
].copy()


# ==========================================
# CREATE LAG FEATURES
# ==========================================

for lag in range(1, LAG_STEPS + 1):

    data[
        f"cpu_lag_{lag}"
    ] = data[
        "cpu_percent"
    ].shift(lag)

    data[
        f"memory_lag_{lag}"
    ] = data[
        "memory_percent"
    ].shift(lag)


# ==========================================
# CREATE NEXT-STEP TARGETS
# ==========================================

data[
    "target_cpu"
] = data[
    "cpu_percent"
].shift(-1)

data[
    "target_memory"
] = data[
    "memory_percent"
].shift(-1)


# ==========================================
# REMOVE INVALID ROWS
# ==========================================

data = data.dropna()


# ==========================================
# SAVE
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

data.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# SUMMARY
# ==========================================

print()
print(
    "ENACT PREDICTION DATASET CREATED"
)

print(
    f"Rows: {len(data)}"
)

print(
    f"Columns: {len(data.columns)}"
)

print(
    f"Time range: "
    f"{data['timestamp'].min()} "
    f"to "
    f"{data['timestamp'].max()}"
)

print(
    f"Saved to: "
    f"{OUTPUT_FILE}"
)

print()
print("Columns:")

for column in data.columns:

    print(
        f"  {column}"
    )