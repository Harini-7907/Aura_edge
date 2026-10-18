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
    / "aura_vs_reactive_memory.png"
)


# ---------------------------------------------------------
# Load results
# ---------------------------------------------------------

df = pd.read_csv(RESULTS_FILE)


# ---------------------------------------------------------
# Get memory values
# ---------------------------------------------------------

aura_memory = float(
    df.loc[
        df["Metric"] == "Average Memory at Migration (%)",
        "AURA-Edge"
    ].iloc[0]
)

reactive_memory = float(
    df.loc[
        df["Metric"] == "Average Memory at Migration (%)",
        "Reactive"
    ].iloc[0]
)


# ---------------------------------------------------------
# Graph data
# ---------------------------------------------------------

strategies = [
    "AURA-Edge",
    "Reactive"
]

memory_values = [
    aura_memory,
    reactive_memory
]


# ---------------------------------------------------------
# Create graph
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    strategies,
    memory_values
)

plt.ylabel(
    "Average Memory at Migration (%)"
)

plt.xlabel(
    "Scheduling Strategy"
)

plt.title(
    "AURA-Edge vs Reactive: Memory at Migration"
)

plt.ylim(
    0,
    100
)


# ---------------------------------------------------------
# Add values
# ---------------------------------------------------------

for bar, value in zip(
    bars,
    memory_values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.2f}%",
        ha="center"
    )


# ---------------------------------------------------------
# Save
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
print("MEMORY COMPARISON GRAPH CREATED")
print("=" * 50)

print(
    f"AURA-Edge Memory: {aura_memory:.2f}%"
)

print(
    f"Reactive Memory: {reactive_memory:.2f}%"
)

print(
    f"Graph saved to: {OUTPUT_FILE}"
)