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
    / "aura_vs_reactive_battery.png"
)


# ---------------------------------------------------------
# Load results
# ---------------------------------------------------------

df = pd.read_csv(RESULTS_FILE)


# ---------------------------------------------------------
# Get battery values
# ---------------------------------------------------------

aura_battery = float(
    df.loc[
        df["Metric"] == "Average Battery at Migration (%)",
        "AURA-Edge"
    ].iloc[0]
)

reactive_battery = float(
    df.loc[
        df["Metric"] == "Average Battery at Migration (%)",
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

battery_values = [
    aura_battery,
    reactive_battery
]


# ---------------------------------------------------------
# Create graph
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    strategies,
    battery_values
)

plt.ylabel(
    "Average Battery at Migration (%)"
)

plt.xlabel(
    "Scheduling Strategy"
)

plt.title(
    "AURA-Edge vs Reactive: Battery at Migration"
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
    battery_values
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
print("BATTERY COMPARISON GRAPH CREATED")
print("=" * 50)

print(
    f"AURA-Edge Battery: {aura_battery:.2f}%"
)

print(
    f"Reactive Battery: {reactive_battery:.2f}%"
)

print(
    f"Graph saved to: {OUTPUT_FILE}"
)