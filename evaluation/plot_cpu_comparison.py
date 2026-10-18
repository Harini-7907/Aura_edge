import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "final_comparison.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "aura_vs_reactive_cpu.png"
)


# ---------------------------------------------------------
# Load final comparison results
# ---------------------------------------------------------

df = pd.read_csv(RESULTS_FILE)


# ---------------------------------------------------------
# Get CPU values
# ---------------------------------------------------------

aura_cpu = float(
    df.loc[
        df["Metric"] == "Average CPU at Migration (%)",
        "AURA-Edge"
    ].iloc[0]
)

reactive_cpu = float(
    df.loc[
        df["Metric"] == "Average CPU at Migration (%)",
        "Reactive"
    ].iloc[0]
)


# ---------------------------------------------------------
# Prepare graph data
# ---------------------------------------------------------

strategies = [
    "AURA-Edge",
    "Reactive"
]

cpu_values = [
    aura_cpu,
    reactive_cpu
]


# ---------------------------------------------------------
# Create graph
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    strategies,
    cpu_values
)

plt.ylabel(
    "Average CPU at Migration (%)"
)

plt.xlabel(
    "Scheduling Strategy"
)

plt.title(
    "AURA-Edge vs Reactive: CPU at Migration"
)

plt.ylim(
    0,
    100
)


# ---------------------------------------------------------
# Add values above bars
# ---------------------------------------------------------

for bar, value in zip(
    bars,
    cpu_values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.2f}%",
        ha="center"
    )


# ---------------------------------------------------------
# Save graph
# ---------------------------------------------------------

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# Confirmation
# ---------------------------------------------------------

print("=" * 50)
print("CPU COMPARISON GRAPH CREATED")
print("=" * 50)

print(
    f"AURA-Edge CPU: {aura_cpu:.2f}%"
)

print(
    f"Reactive CPU: {reactive_cpu:.2f}%"
)

print(
    f"Graph saved to: {OUTPUT_FILE}"
)