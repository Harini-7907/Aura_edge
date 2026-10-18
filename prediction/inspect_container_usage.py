import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "data/raw/alibaba_clusterdata_v2018/container_usage.csv"
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

print("Inspecting corrected Alibaba container usage data...")

df = pd.read_csv(
    INPUT_FILE,
    header=None,
    names=COLUMNS,
    nrows=20
)

# Remove the unused first column
df = df.drop(columns=["unused"])

print("\n==========================================")
print("CORRECTED CONTAINER USAGE DATA")
print("==========================================")

print("\nShape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 20 rows:")
print(df.to_string(index=False))

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nBasic statistics:")
print(df.describe())