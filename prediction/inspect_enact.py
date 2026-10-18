import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENACT_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "enact"
)


# ---------------------------------------------------------
# Files to inspect
# ---------------------------------------------------------

files = [
    "node_telemetry_pods_off.csv",
    "node_telemetry_pods_on.csv",
    "pod_telemetry_pods_off.csv",
    "pod_telemetry_pods_on.csv"
]


# ---------------------------------------------------------
# Inspect each file
# ---------------------------------------------------------

for filename in files:

    file_path = ENACT_FOLDER / filename

    print()
    print("=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)

    # Read only a small sample
    df = pd.read_csv(
        file_path,
        nrows=5
    )

    print()
    print("Columns:")
    print(df.columns.tolist())

    print()
    print("Shape of sample:")
    print(df.shape)

    print()
    print("Data types:")
    print(df.dtypes)

    print()
    print("First 5 rows:")
    print(df.to_string(index=False))