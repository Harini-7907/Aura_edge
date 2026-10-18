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

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


# ---------------------------------------------------------
# ENACT node files
# ---------------------------------------------------------

FILES = [
    "node_telemetry_pods_off.csv",
    "node_telemetry_pods_on.csv"
]


# ---------------------------------------------------------
# Columns required by AURA-Edge
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "node_name",
    "timestamp",
    "CPU (%)",
    "MEM (%)",
    "fs (%)",
    "Energy (watts)",
    "rx (B/sec)",
    "tx (B/sec)"
]


# ---------------------------------------------------------
# Prepare one ENACT file
# ---------------------------------------------------------

def prepare_file(filename):

    input_file = ENACT_FOLDER / filename

    print()
    print("=" * 70)
    print(f"Processing: {filename}")
    print("=" * 70)

    # Load data
    df = pd.read_csv(input_file)

    # Check columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Keep only required columns
    df = df[REQUIRED_COLUMNS].copy()

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Convert numerical columns
    numerical_columns = [
        "CPU (%)",
        "MEM (%)",
        "fs (%)",
        "Energy (watts)",
        "rx (B/sec)",
        "tx (B/sec)"
    ]

    for column in numerical_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid rows
    df = df.dropna()

    # Sort by node and time
    df = df.sort_values(
        ["node_name", "timestamp"]
    )

    # Reset index
    df = df.reset_index(drop=True)

    # Create output folder
    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # Output filename
    output_name = filename.replace(
        ".csv",
        "_clean.csv"
    )

    output_file = OUTPUT_FOLDER / output_name

    # Save
    df.to_csv(
        output_file,
        index=False
    )

    # Summary
    print()
    print(f"Rows: {len(df)}")
    print(
        f"Nodes: {df['node_name'].nunique()}"
    )
    print(
        f"Time range: "
        f"{df['timestamp'].min()} "
        f"to "
        f"{df['timestamp'].max()}"
    )

    print()
    print("CPU statistics:")
    print(df["CPU (%)"].describe())

    print()
    print("Memory statistics:")
    print(df["MEM (%)"].describe())

    print()
    print("Energy statistics:")
    print(df["Energy (watts)"].describe())

    print()
    print(
        f"Saved to: {output_file}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("ENACT NODE TELEMETRY PREPROCESSING")
    print("=" * 70)

    for filename in FILES:

        prepare_file(filename)

    print()
    print("=" * 70)
    print("ENACT PREPROCESSING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":

    main()